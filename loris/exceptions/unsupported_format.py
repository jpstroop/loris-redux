from loris.exceptions.loris_exception import LorisException

class UnsupportedFormat(LorisException):
    def __init__(self, message, http_status_code=404):
        super().__init__(message, http_status_code)
