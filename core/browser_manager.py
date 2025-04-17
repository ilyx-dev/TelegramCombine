from models.ads_profile import AdsProfile
from core.api.ads_local_api import AdsLocalApi


class BrowserManager:
    def __init__(self, local_api: AdsLocalApi):
        self._local_api = local_api

    def get_managed_profile(self, serial_number: int, headless_mode: bool = False):
        return AdsProfile(serial_number, self._local_api, headless_mode)
