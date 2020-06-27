##########
# Types of Errors
##########


class Error():
    def __init__(self, _name, _info):
        self.name = _name
        self.info = _info

    def __str__(self):
        return f'{self.name}: {self.info}'


class InvalidCharError(Error):
    def __init__(self, _info):
        super().__init__('Invalid Char', _info)


class InterpreterError(Error):
    def __init__(self, info_):
        super().__init__('Runtime error', info_)
