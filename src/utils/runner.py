from typing import Optional, Literal

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


async def _upload_file(route: Route, module: Literal["allowlist", "subscription"]) -> Optional[bool]:
    uploader = FileUploader(private_key=route.wallet.private_key, proxy=route.wallet.proxy, module=module)
    logger.debug(uploader)
    if await uploader.upload_file(module=module):
        return True


async def process_allowlist_file_upload(route: Route) -> Optional[bool]:
    return await _upload_file(route, "allowlist")


async def process_subscription_file_upload(route: Route) -> Optional[bool]:
    return await _upload_file(route, "subscription")
