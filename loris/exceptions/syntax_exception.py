from loris.exceptions.loris_exception import LorisException

class SyntaxException(LorisException):
    # Raise when a parameter can't be parsed.
    def __init__(self, value, http_status_code=400):
        super().__init__(value, http_status_code)
