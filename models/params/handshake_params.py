class HandshakeParams(object):
    def __init__(self):
        self.key: str = ""

    def set_key(self, key: str):
        self.key = f"-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----\n"

    def get_key(self) -> str:
        return self.key
