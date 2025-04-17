import logging
from playwright.async_api import BrowserContext, Page

from modules.blum.initial_action import InitialAction
from modules.blum.tasks import BlumTasks
from modules.imodule import IModule

logger = logging.getLogger(__name__)

class BlumModule(IModule):
    def __init__(self, context: BrowserContext, page: Page, config: dict):
        super().__init__(context, page, config)

    async def execute(self):
        await super().execute()
        initial_action = InitialAction(self._frame)
        await initial_action.handle_initial_action()

        tasks = BlumTasks(self._frame)