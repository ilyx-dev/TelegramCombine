import asyncio
import logging
from contextvars import ContextVar

import config
from config import *
from core.api.ads_local_api import AdsLocalApi
from core.browser_manager import BrowserManager
from core.telegram_manager import TelegramManager
from utils import helpers

account_number_var = ContextVar("account_number", default="unknown")

old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)

    record.account_number = account_number_var.get()
    return record

logging.setLogRecordFactory(record_factory)

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | Account %(account_number)s | %(message)s')

logger = logging.getLogger(__name__)

async def main():
    accounts_numbers = helpers.read_from_file(accounts_file)
    modules = config.modules_data

    dolphin_local_api = AdsLocalApi(port)
    dolphin_manager = BrowserManager(dolphin_local_api)

    for account_number in accounts_numbers:
        account_number_var.set(account_number)

        async with dolphin_manager.get_managed_profile(account_number) as context:
            if not await helpers.check_proxy(context.pages[0]):
                logger.error('Proxy not working')
                continue

            telegram_manager = await TelegramManager.init(context)
            if not await telegram_manager.check_authorization():
                logger.error('Telegram account not authorized')
                continue

            await helpers.close_all_pages(context)

            for module_name, module_data in modules.items():
                module_class = module_data['class']
                module_config = module_data.copy()
                module_config.pop('class', None)

                module = await module_class.init(context, module_config)
                await module.navigate()
                await module.execute()

if __name__ == "__main__":
    asyncio.run(main())