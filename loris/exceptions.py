from collections import OrderedDict
from json import dumps
from loris.constants import URI_COMPLIANCE_PAGE


class LorisException(Exception):
    def __init__(self, message, http_status_code):
        self.http_status_code = http_status_code
        self.message = message

    def __str__(self):
        return self.to_json()

    def to_json(self):
        return dumps(self._to_dict())

    def _to_dict(self):
        d = OrderedDict()
        d["error"] = self.__class__.__name__
        d["description"] = self.message
        return d


class ResolverException(LorisException):
    def __init__(self, identifier):
        http_status_code = 404
        message = f"Could not resolve identifier: {identifier}"
        super().__init__(message, http_status_code)


class UnsupportedFormat(LorisException):
    # The when we can't work with the image on the server.
    def __init__(self, message, http_status_code=500):
        super().__init__(message, http_status_code)


class SyntaxException(LorisException):
    # Raise when a parameter can't be parsed.
    def __init__(self, value, http_status_code=400):
        super().__init__(value, http_status_code)


class RequestException(LorisException):
    # Use for, e.g. out of bounds requests, unavailable qualities
    def __init__(self, message, http_status_code=400):
        super().__init__(message, http_status_code)


class FeatureNotEnabledException(RequestException):
    # Use for requests that require IIIF features that are disabled in the config.
    def __init__(self, feature):
        self.feature = feature
        message = (
            f"Server does not support the '{feature}' feature."
            f" See {URI_COMPLIANCE_PAGE} for details."
        )
        super().__init__(message, 501)
