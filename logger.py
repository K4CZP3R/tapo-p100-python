import inspect
from typing import Any


class Logger:
    def __init__(self, module_name: str):
        self.module_name: str = module_name

    def out(self, content: Any):
        calling_function = inspect.stack()[1].function
        print(f"[{self.module_name}] <{calling_function}> {content}")
