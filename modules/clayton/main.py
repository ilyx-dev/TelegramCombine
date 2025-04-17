import logging

from playwright.async_api import BrowserContext, Page

from modules.imodule import IModule

logger = logging.getLogger(__name__)

class ClaytonModule(IModule):
    def __init__(self, context: BrowserContext, page: Page, config: dict):
        super().__init__(context, page, config)

    async def execute(self):
        await super().execute()

