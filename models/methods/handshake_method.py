from models.methods import method
from typing import Any

class HandshakeMethod(method.Method):
    def __init__(self, params: Any):
        super().__init__("handshake", params)


