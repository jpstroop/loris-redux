from loris.exceptions.request_exception import RequestException

class FeatureNotEnabledException(RequestException):
    # Use for requests that require IIIF features that disabled in the config. 
    def __init__(self, message, feature, http_status_code=400):
        self.feature = feature
        super().__init__(message, http_status_code)
