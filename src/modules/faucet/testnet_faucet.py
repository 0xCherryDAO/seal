from typing import Optional

import pyuseragents
from loguru import logger

from config import CAPSOLVER_API
from src.utils.captcha_solver.solver import CaptchaSolver
from src.utils.proxy_manager import Proxy
from src.utils.request_client.curl_cffi_client import CurlCffiClient
from src.utils.user.sui_account import SuiAccount


class Faucet(SuiAccount, CurlCffiClient):
    def __init__(
            self,
            private_key: str,
            proxy: Proxy | None
    ):
        SuiAccount.__init__(self, mnemonic=private_key)
        CurlCffiClient.__init__(self, proxy=proxy)
        self.captcha_solver = CaptchaSolver(capsolver_api=CAPSOLVER_API, proxy=proxy)

    def __str__(self) -> str:
        return f'[{self.wallet_address}] | Requesting tokens from faucet...'

    async def request_tokens(self) -> Optional[bool]:
        logger.debug(f'Solving Cloudflare...')
        captcha_token = await self.captcha_solver.solve_turnstile(
            page_url='https://faucet.sui.io/',
            sitekey='0x4AAAAAAA11HKyGNZq_dUKj'
        )
        if captcha_token:
            logger.success(f'Successfully solved Cloudflare')

        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://faucet.sui.io',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': pyuseragents.random(),
            'x-turnstile-token': captcha_token,
        }

        json_data = {
            'FixedAmountRequest': {
                'recipient': str(self.wallet_address),
            },
        }

        response_json, status = await self.make_request(
            method="POST",
            url='https://faucet.testnet.sui.io/v2/faucet_web_gas',
            headers=headers,
            json=json_data
        )
        if status == 200:
            logger.success(f'[{self.wallet_address}] | Successfully requested testnet SUI!')
            return True
        elif status == 429:
            logger.warning(f'[{self.wallet_address}] | Already requested tokens. Wait for cooldown.')
        else:
            logger.error(f'[{self.wallet_address}] | Unknown error | Status code: {status}')
