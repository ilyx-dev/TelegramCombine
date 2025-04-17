from playwright.async_api import async_playwright

from core.api.ads_local_api import AdsLocalApi


class AdsProfile:
    def __init__(self, serial_number: int, local_api: AdsLocalApi, headless_mode: bool):
        self.serial_number = serial_number
        self.local_api = local_api
        self.headless_mode = headless_mode

    async def __aenter__(self):
        ws_endpoint = await self.local_api.start_profile(self.serial_number, self.headless_mode)

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.connect_over_cdp(ws_endpoint)
        self.context = self.browser.contexts[0]
        return self.context

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.local_api.stop_profile(self.serial_number)
        except Exception:
            pass
