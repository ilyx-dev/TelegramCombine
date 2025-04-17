# Telegram Mini-Apps Automation Software

## Project Description

This project is an asynchronous, modular software for automating Telegram mini-apps using the AdsPower anti-detect browser and the Playwright library. It is designed with maximum modularity, allowing easy integration of other anti-detect browsers and the addition of new modules for different Telegram mini-apps.

The program can handle multiple accounts simultaneously, check proxy functionality, verify Telegram authorization, and perform automated actions in mini-apps based on specified modules.

## Features

- **Modular Architecture**: Add new Telegram mini-apps by creating classes that inherit from the `IModule` interface.
- **Multi-Account Support**: Automate actions for multiple accounts listed in the `serial_numbers.txt` file.
- **Proxy Validation**: Automatically checks the functionality of proxies for each account.
- **Telegram Authorization Check**: Ensures the account is authorized in Telegram before starting operations.
- **Flexible Configuration**: Configured via `config.py`, supporting modules, domains, app names, and referral codes.
- **Error Handling**: Uses a `retry` decorator for retrying operations during temporary failures.
- **Logging**: Detailed logging with account numbers for easy debugging.

## Requirements

- Python 3.8 or higher
- AdsPower installed and running with local API access (default port: 50325)
- Installed dependencies:
  - `playwright` (`pip install playwright`)
  - `aiohttp` (`pip install aiohttp`)
  - Additional libraries listed in `requirements.txt` (recommended to create this file)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure AdsPower is running and the local API is accessible on the specified port.

## Configuration

### 1. File `config.py`

This file contains the main program settings:

- `port`: Port for the AdsPower local API (default: 50325).
- `accounts_file`: Path to the file containing account serial numbers (`data/serial_numbers.txt`).
- `modules_data`: A dictionary with module settings, specifying for each module:
  - `class`: The module class (e.g., `BlumModule`).
  - `domain`: The mini-app domain in Telegram.
  - `appname`: The app name.
  - `iframe_selector`: The iframe selector for interacting with the app.
  - `referral_codes`: A list of referral codes to use.

Example:

```python
from modules.blum.main import BlumModule
from modules.clayton.main import ClaytonModule

port = 50325
accounts_file = 'data/serial_numbers.txt'

modules_data = {
    "blum": {
        "class": BlumModule,
        "domain": "blum",
        "appname": "app",
        "iframe_selector": "iframe.payment-verification",
        "referral_codes": ["ref_NrOGHTSwQw"]
    },
    "clayton": {
        "class": ClaytonModule,
        "domain": "claytoncoinbot",
        "appname": "game",
        "iframe_selector": "iframe.payment-verification",
        "referral_codes": ["7267714184"]
    }
}
```

### 2. File `data/serial_numbers.txt`

A text file containing account serial numbers (one per line). Example:

```
1001
1002
1003
```

## Usage

1. Configure `config.py` and ensure the `serial_numbers.txt` file is populated.
2. Run the program:

   ```bash
   python main.py
   ```

3. The program will:
   - Read the account serial numbers.
   - Launch a browser profile for each account via AdsPower.
   - Verify proxies and Telegram authorization.
   - Execute actions for each specified module.

Logs will be displayed in the console, including the account number and execution status.

## How to Add a New Module

To add support for a new Telegram mini-app:

1. Create a new file in the `modules` directory, e.g., `modules/newapp/main.py`.

2. Define a class inheriting from `IModule` and implement the `execute` method:

   ```python
   from modules.imodule import IModule
   
   class NewAppModule(IModule):
       async def execute(self):
           await super().execute()
           # Add automation logic here
           logger.info("Executing actions for NewApp")
   ```

3. Update `config.py` to include the new module:

   ```python
   from modules.newapp.main import NewAppModule
   
   modules_data = {
       # Existing modules...
       "newapp": {
           "class": NewAppModule,
           "domain": "newappdomain",
           "appname": "newappname",
           "iframe_selector": "iframe.selector",
           "referral_codes": ["ref_code1", "ref_code2"]
       }
   }
   ```

4. Add additional classes or functions for the module if needed.

The new module will be automatically used by the program upon launch.

## How to Use a Different Anti-Detect Browser

The software is designed to support different anti-detect browsers through an API abstraction.

1. Create a new API class in `core/api/`, e.g., `new_browser_api.py`, similar to `ads_local_api.py`:

   ```python
   import aiohttp
   from utils.decorators import retry
   
   class NewBrowserApi:
       def __init__(self, port):
           self.port = port
   
       @retry()
       async def start_profile(self, serial_number: int, headless: bool = False):
           # Logic for starting a profile in the new browser
           async with aiohttp.request('GET', f"http://localhost:{self.port}/start?profile={serial_number}") as response:
               response_json = await response.json()
               return response_json['ws_endpoint']
   
       async def stop_profile(self, serial_number: int):
           # Logic for stopping a profile
           async with aiohttp.request('GET', f"http://localhost:{self.port}/stop?profile={serial_number}") as response:
               pass
   ```

2. Update `BrowserManager` in `core/browser_manager.py` to work with the new API:

   ```python
   from core.api.new_browser_api import NewBrowserApi
   
   class BrowserManager:
       def __init__(self, local_api: NewBrowserApi):
           self._local_api = local_api
   ```

3. Modify `main.py` to use the new API:

   ```python
   from core.api.new_browser_api import NewBrowserApi
   
   async def main():
       local_api = NewBrowserApi(port)
       dolphin_manager = BrowserManager(local_api)
       # The rest of the code remains unchanged
   ```

The program will now work with the new anti-detect browser.

## Features

- **Asynchronous Design**: Uses `asyncio` for efficient handling of multiple accounts.
- **Context Managers**: `AdsProfile` automatically manages profile start and stop.
- **Logging**: Each log includes the account number for easy tracking.
- **Flexible URLs**: Modules generate mini-app URLs based on configuration.

## Logging and Error Handling

- Logging is configured using `logging` with a custom format that includes the account number.
- The `retry` decorator in `utils/decorators.py` ensures retries with exponential backoff for transient failures.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit changes with descriptive messages.
4. Submit a pull request.

## License

This project is licensed under the MIT License.
