from asyncio import sleep

from config import CAPSOLVER_API
from src.utils.proxy_manager import Proxy
from src.utils.request_client.tls import TlsClient


class CaptchaSolver(TlsClient):
    def __init__(
            self,
            capsolver_api: str = CAPSOLVER_API,
            proxy: Proxy | None = None
    ):
        self.api = capsolver_api
        super().__init__(proxy=proxy)

    async def solve_turnstile(self, page_url: str, sitekey: str) -> str:
        payload = {
            "clientKey": self.api,
            "task": {
                "type": "AntiTurnstileTaskProxyLess",
                "websiteURL": page_url,
                "websiteKey": sitekey,
            }
        }

        response_json, status = await self.make_request(
            method="POST",
            url='https://api.capsolver.com/createTask',
            json=payload
        )
        captcha_id = response_json['taskId']

        while True:
            await sleep(5)
            payload = {
                "clientKey": self.api,
                "taskId": captcha_id
            }
            response_json, status = await self.make_request(
                method="POST",
                url=f"https://api.capsolver.com/getTaskResult",
                json=payload
            )
            if response_json['status'] == 'ready':
                return response_json['solution']['token']
