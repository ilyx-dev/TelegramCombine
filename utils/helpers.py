import logging
import random

import aiohttp

logger = logging.getLogger(__name__)

def read_from_file(path):
    with open(path, 'r') as file:
        return [line.strip() for line in file.readlines()]

async def close_all_pages(context):
    pages = context.pages
    if len(pages) > 2:
        for page in pages[2:]:
            await page.close()

async def get_nickname_from_randommer():
    data = {
        'culture': 'en_US',
        'firstname': '',
        'lastname': ''
    }
    async with aiohttp.request('POST', 'https://randommer.io/username-generator', data=data) as response:
        response_data = await response.json()
        return random.choice(response_data)


async def check_proxy(page):
    try:
        response = await page.evaluate('''() => {
                return fetch('https://api.ipify.org?format=json')
                    .then(response => response.json())
                    .then(data => data.ip)
                    .catch(() => null);
            }''')

        if response:
            logger.info(f"Proxy IP address: {response}")
            return True
        else:
            return False
    except Exception as e:
        return False