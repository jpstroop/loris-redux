from loris.exceptions.request_exception import RequestException

COMPLIANCE_PAGE = 'http://iiif.io/api/image/2.1/compliance/#compliance'

class FeatureNotEnabledException(RequestException):
    # Use for requests that require IIIF features that are disabled in the config.
    def __init__(self, feature):
        self.feature = feature
        message = "Server does not support the '{0}' feature.".format(feature)
        message += ' See {0} for details.'.format(COMPLIANCE_PAGE)
        super().__init__(message)
