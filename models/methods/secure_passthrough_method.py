from models.methods import method
from typing import Any

class SecurePassthroughMethod(method.Method):
    def __init__(self, params: Any):
        super().__init__("securePassthrough", {"request": params})

