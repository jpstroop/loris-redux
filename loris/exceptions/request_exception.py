from loris.exceptions.loris_exception import LorisException

class RequestException(LorisException):
    # Use for, e.g. out of bounds requests, unavailable qualities
    def __init__(self, message, http_status_code=400):
        super().__init__(message, http_status_code)
