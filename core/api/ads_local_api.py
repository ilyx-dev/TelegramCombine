import logging

import aiohttp

from utils.decorators import retry
from utils.exceptions import BrowserStartException, BrowserStopException

logger = logging.getLogger(__name__)

class AdsLocalApi:
    def __init__(self, port):
        self.port = port

    @retry(logger=logger)
    async def start_profile(self, serial_number: int, headless: bool = False):
        async with aiohttp.request('GET', f"http://local.adspower.net:{self.port}/api/v1/browser/start?serial_number={serial_number}&headless={1 if headless else 0}&open_tabs=1") as response:
            response.raise_for_status()

            response_json = await response.json()
            if response_json['code'] != 0:
                raise BrowserStartException(response_json['msg'])
            else:
                return response_json['data']['ws']['puppeteer']

    async def stop_profile(self, serial_number: int):
        async with aiohttp.request('GET', f"http://local.adspower.net:{self.port}/api/v1/browser/stop?serial_number={serial_number}") as response:
            response.raise_for_status()

            response_json = await response.json()
            if response_json['code'] != 0:
                raise BrowserStopException(response_json['msg'])
