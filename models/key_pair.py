class KeyPair(object):
    def __init__(self, private_key: str, public_key: str):
        self.private_key = private_key
        self.public_key = public_key

    def get_private_key(self):
        return self.private_key

    def get_public_key(self):
        return self.public_key
