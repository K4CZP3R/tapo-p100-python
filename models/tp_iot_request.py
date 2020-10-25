from typing import Any


class TPIoTRequest(object):
    def __init__(self):
        self.method: str = ""
        self.params: Any = None
        self.requestID: float = 0
        self.requestTimeMils: float = 0
        self.terminalUUID: str = ""

    def set_method(self, method: str):
        self.method = method

    def set_params(self, params: Any):
        self.params = params

    def set_request_time_mils(self, request_time_mils:float):
        self.requestTimeMils = request_time_mils
