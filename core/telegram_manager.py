import json

from playwright.async_api import BrowserContext


class TelegramManager:
    def __init__(self, page):
        self._page = page

    @classmethod
    async def init(cls, context: BrowserContext):
        _page = await context.new_page()
        return cls(_page)

    async def check_authorization(self) -> bool:
        await self._page.goto('https://web.telegram.org/k/')
        await self._page.wait_for_function("document.readyState === 'complete'")

        user_auth_key = await self._page.evaluate("window.localStorage.getItem('user_auth')")
        if user_auth_key is not None:
            user_auth = json.loads(user_auth_key)
            if user_auth.get('id') is not None:
                return True
            else:
                return False
        else:
            return False
