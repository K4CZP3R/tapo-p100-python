class LoginDeviceParams(object):
    def __init__(self):
        self.password: str = ""
        self.username: str = ""

    def set_password(self, password: str):
        self.password = password

    def set_username(self, username: str):
        self.username = username

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password
