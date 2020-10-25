import requests
from typing import Any

class Http:
    @staticmethod
    def make_post(url, json: Any) -> requests.Response:
        return requests.post(url, json=json)

    @staticmethod
    def make_post_cookie(url, json, cookie) -> requests.Response:
        return requests.post(url, json=json, cookies=cookie)
