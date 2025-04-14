import random
import string
from asyncio import sleep
from typing import Optional

import pyuseragents
from loguru import logger
from pysui.sui.sui_txn.async_transaction import SuiTransactionAsync
from pysui.sui.sui_types import SuiString

from src.utils.common.wrappers.decorators import retry
from src.utils.proxy_manager import Proxy
from src.utils.request_client.curl_cffi_client import CurlCffiClient
from src.utils.user.sui_account import SuiAccount


class FileUploader(SuiAccount, CurlCffiClient):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None
    ):
        SuiAccount.__init__(self, mnemonic=private_key)
        CurlCffiClient.__init__(self, proxy=proxy)

    @staticmethod
    def generate_name() -> str:
        characters = string.ascii_lowercase
        length = random.randint(5, 8)
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def encode_image_to_bytes(image_path: str):
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
        return image_bytes

    async def create_allowlist_entry(self, entry_name: str):
        tx = SuiTransactionAsync(client=self.client)

        await tx.move_call(
            target=SuiString(
                f"0x4cb081457b1e098d566a277f605ba48410e26e66eaab5b3be4f6c560e9501800::allowlist::create_allowlist_entry"
            ),
            arguments=[
                SuiString(entry_name)
            ]
        )
        simulation_status = await self.simulate_tx(tx)
        if simulation_status is False:
            logger.error(f'[{self.wallet_address}] | TX failed while simulating entry creation')
            return False

        status, digest = await self.send_tx(tx)
        if status is True:
            logger.success(
                f'[{self.wallet_address}] | Successfully created entry with name {entry_name} '
                f'| TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            return True
        logger.error(
            f'[{self.wallet_address}] | Failed to create entry | TX: https://testnet.suivision.xyz/txblock/{digest}'
        )
        await sleep(0.1)

    async def check_if_address_already_added(self, object_id: str):
        sui_object = await self.client.get_object(object_id)
        data = sui_object.result_data.to_dict()
        if str(self.wallet_address) in data['content']['fields']['list']:
            return True

    async def get_objects(self) -> Optional[tuple[str, str]]:
        objects = await self.client.get_objects(self.wallet_address, fetch_all=True)
        data = objects.result_data.to_dict()['data']
        for sui_object in data:
            if sui_object[
                'type'
            ] == '0x4cb081457b1e098d566a277f605ba48410e26e66eaab5b3be4f6c560e9501800::allowlist::Cap':
                address_already_added = await self.check_if_address_already_added(
                    sui_object['content']['fields']['allowlist_id']
                )
                if address_already_added:
                    await sleep(0.1)
                    continue
                await sleep(10)
                return sui_object['content']['fields']['allowlist_id'], sui_object['content']['fields']['id']

    async def add_address(self, allowlist_id: str, object_id: str):
        allowlist_object = await self.client.get_object(allowlist_id)
        entry_object = await self.client.get_object(object_id)

        while True:
            tx = SuiTransactionAsync(client=self.client)
            await tx.move_call(
                target=SuiString(
                    f"0x4cb081457b1e098d566a277f605ba48410e26e66eaab5b3be4f6c560e9501800::allowlist::add"
                ),
                arguments=[
                    allowlist_object.result_data,
                    entry_object.result_data,
                    self.wallet_address
                ]
            )
            # simulation_status = await self.simulate_tx(tx)
            # if simulation_status is False:
            #     logger.error(f'[{self.wallet_address}] | TX failed while simulating address adding')
            #     return False

            status, digest = await self.send_tx(tx)
            if status is True:
                logger.success(
                    f'[{self.wallet_address}] | Successfully added address into entry '
                    f'| TX: https://testnet.suivision.xyz/txblock/{digest}'
                )
                return True
            logger.error(
                f'[{self.wallet_address}] | Failed to add address into entry | TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            await sleep(1)
            continue

    async def get_blob_id(self, data: bytes):
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'origin': 'https://seal-example.vercel.app',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': pyuseragents.random(),
            'content-type': 'application/x-www-form-urlencoded',
        }

        params = {
            'epochs': '1',
        }

        response_json, status = await self.make_request(
            method="PUT",
            url='https://seal-example.vercel.app/publisher1/v1/blobs',
            params=params,
            headers=headers,
            data=data
        )
        if status == 200:
            try:
                return response_json['newlyCreated']['blobObject']['blobId']
            except KeyError:
                if response_json['alreadyCertified']:
                    logger.warning(f'File has been already uploaded')

    async def upload_blob(self, allowlist_id: str, object_id: str, blob_id: str):
        tx = SuiTransactionAsync(client=self.client)
        allowlist_object = await self.client.get_object(allowlist_id)
        entry_object = await self.client.get_object(object_id)

        await tx.move_call(
            target=SuiString(
                f"0x4cb081457b1e098d566a277f605ba48410e26e66eaab5b3be4f6c560e9501800::allowlist::publish"
            ),
            arguments=[
                allowlist_object.result_data,
                entry_object.result_data,
                SuiString(blob_id)
            ]
        )
        simulation_status = await self.simulate_tx(tx)
        if simulation_status is False:
            logger.error(f'[{self.wallet_address}] | TX failed while simulating publish')
            return False

        status, digest = await self.send_tx(tx)
        if status is True:
            logger.success(
                f'[{self.wallet_address}] | Successfully published! '
                f'| TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            return True
        logger.error(
            f'[{self.wallet_address}] | Failed to publish | TX: https://testnet.suivision.xyz/txblock/{digest}'
        )
        await sleep(0.1)

    @retry()
    async def upload_file(self) -> Optional[bool]:
        entry_name = self.generate_name()
        await self.create_allowlist_entry(entry_name)
        await sleep(4)
        allowlist_id, object_id = await self.get_objects()

        await self.add_address(allowlist_id, object_id)

        image_data = self.encode_image_to_bytes('Screenshot_000.png')
        blob_id = await self.get_blob_id(image_data)
        if not blob_id:
            return None
        return await self.upload_blob(allowlist_id, object_id, blob_id)
