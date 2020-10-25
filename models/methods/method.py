class Method(object):
    def __init__(self, method, params):
        self.method = method
        self.params = params

    def get_params(self):
        return self.params

    def get_method(self):
        return self.method