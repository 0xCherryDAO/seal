import platform
from typing import Dict, Any

from curl_cffi.requests import AsyncSession, BrowserType

from src.utils.proxy_manager import Proxy


class CurlCffiClient:
    def __init__(self, proxy: Proxy | None):
        self.session = AsyncSession(
            proxies={
                'http': proxy.proxy_url if proxy else None,
                'https': proxy.proxy_url if proxy else None
            },
            impersonate=BrowserType.chrome124 if platform.system() == 'Windows' else BrowserType.chrome131
        )

    async def make_request(
            self,
            method: str = 'GET',
            url: str = None,
            headers: Dict[str, Any] = None,
            data: str | bytes = None,
            json: Dict[str, Any] = None,
            params: Dict[str, Any] = None,
            cookies: Dict[str, Any] = None,
            return_text: bool = False
    ):
        response = await self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            json=json,
            cookies=cookies
        )
        if response.status_code in [200, 201]:
            if return_text:
                return response.text, response.status_code
            return response.json(), response.status_code
        else:
            return response.text, response.status_code
