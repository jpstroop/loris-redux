from collections import OrderedDict
from loris.constants import COMPLIANCE_PAGE
import json

class _LorisException(Exception):
    def __init__(self, message, http_status_code):
        self.http_status_code = http_status_code
        self.message = message

    def __str__(self):
        return self.to_json()

    def to_json(self):
        return json.dumps(self._to_dict())

    def _to_dict(self):
        d = OrderedDict()
        d['error'] = self.__class__.__name__
        d['description'] = self.message
        return d

class ResolverException(_LorisException):
    def __init__(self, identifier):
        http_status_code = 404
        message = 'Could not resolve identifier: {0}'.format(identifier)
        super().__init__(message, http_status_code)

class UnsupportedFormat(_LorisException):
    # The when we can't work with the image on the server.
    def __init__(self, message, http_status_code=500):
        super().__init__(message, http_status_code)

class SyntaxException(_LorisException):
    # Raise when a parameter can't be parsed.
    def __init__(self, value, http_status_code=400):
        super().__init__(value, http_status_code)

class RequestException(_LorisException):
    # Use for, e.g. out of bounds requests, unavailable qualities
    def __init__(self, message, http_status_code=400):
        super().__init__(message, http_status_code)

class FeatureNotEnabledException(RequestException):
    # Use for requests that require IIIF features that are disabled in the config.
    def __init__(self, feature):
        self.feature = feature
        message = "Server does not support the '{0}' feature.".format(feature)
        message += ' See {0} for details.'.format(COMPLIANCE_PAGE)
        super().__init__(message)
