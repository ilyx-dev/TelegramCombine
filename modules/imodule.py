import logging
import random
from abc import ABC, abstractmethod

from playwright.async_api import BrowserContext, Page, FrameLocator, Frame

logger = logging.getLogger(__name__)


class IModule(ABC):
    def __init__(self, context: BrowserContext, page: Page, config: dict):
        self._context = context
        self._page = page
        self._config = config
        self._frame: Frame = None

    @classmethod
    async def init(cls, context: BrowserContext, config: dict):
        page = await context.new_page()
        return cls(context, page, config)

    async def navigate(self):
        logger.info(f'Navigate to {self.__class__.__name__}')

        domain = self._config.get('domain')
        appname = self._config.get('appname')
        iframe_selector = self._config.get('iframe_selector')
        startapp_param = random.choice(self._config.get('referral_codes'))

        url = (
            f"https://web.telegram.org/k/#?tgaddr="
            f"tg%3A%2F%2Fresolve%3Fdomain%3D{domain}"
            f"%26appname%3D{appname}%26startapp%3D{startapp_param}"
        )
        await self._page.goto(url)

        launch_button = self._page.locator("//button[.//span[text()='Launch']]")
        await launch_button.click()

        iframe_element = await self._page.wait_for_selector(iframe_selector)
        frame = await iframe_element.content_frame()
        await frame.wait_for_load_state('networkidle')
        self._frame = frame

    @abstractmethod
    async def execute(self):
        logger.info(f'Started {self.__class__.__name__}')
