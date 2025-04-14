from typing import Optional

from loguru import logger

from src.models.route import Route
from src.modules.file_uploader.uploader import FileUploader
from src.modules.faucet.testnet_faucet import Faucet


async def process_faucet(route: Route) -> Optional[bool]:
    faucet = Faucet(
        private_key=route.wallet.private_key,
        proxy=route.wallet.proxy
    )
    logger.debug(faucet)
    requested = await faucet.request_tokens()
    if requested:
        return True


async def process_file_upload(route: Route) -> Optional[bool]:
    uploader = FileUploader(
        private_key=route.wallet.private_key,
        proxy=route.wallet.proxy
    )
    uploaded = await uploader.upload_file()
    if uploaded:
        return True
