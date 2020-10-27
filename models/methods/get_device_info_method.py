from models.methods import method
from typing import Any


class GetDeviceInfoMethod(method.Method):
    def __init__(self, params: Any):
        super().__init__("get_device_info", params)
