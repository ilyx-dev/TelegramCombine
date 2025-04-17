import asyncio
import logging
import random

from playwright.async_api import Frame

from utils.helpers import get_nickname_from_randommer

logger = logging.getLogger(__name__)

class InitialAction:
    def __init__(self, frame: Frame):
        self._frame = frame

    async def _claim_and_start_farming(self):
        farming_button_locator = self._frame.locator("//div[@class='kit-fixed-wrapper has-layout-tabs']//div[@class='index-farming-button']//button")

        while True:
            await farming_button_locator.wait_for(timeout=120 * 1000)
            farming_button_text = (await farming_button_locator.text_content()).strip()

            if "Claim" in farming_button_text:
                await farming_button_locator.click()
                logger.info("The daily reward for farming is received")
                await farming_button_locator.wait_for(state='attached')
            elif "Start farming" in farming_button_text:
                await farming_button_locator.click()
                logger.info("Start farming")
                break
            elif "Farming" in farming_button_text:
                logger.info("The daily reward has already been received. Skipping farming")
                break
            else:
                logger.warning(f"Unexpected farming button text: {farming_button_text}")
                break

    async def handle_initial_action(self):
        # Wait for the page to fully load
        await self._frame.wait_for_load_state('networkidle')

        element_actions = {
            "//div[contains(@class, 'daily-modal-backdrop')]": [self._registration],
            "//button[.//div[text()='Continue']]": [self._collect_daily_reward, self._claim_and_start_farming],
            "//div[@class='index-farming-button']//button": [self._claim_and_start_farming],
        }

        tasks = []
        task_to_actions = {}
        for locator, actions in element_actions.items():
            task = asyncio.create_task(self._frame.wait_for_selector(locator, timeout=120 * 1000))
            tasks.append(task)
            task_to_actions[task] = actions

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        if not done:
            raise TimeoutError("Failed to find any of the specified items within the timeout period")

        completed_task = list(done)[0]
        actions = task_to_actions[completed_task]
        for action in actions:
            await action()
            await asyncio.sleep(3)

        for task in pending:
            task.cancel()