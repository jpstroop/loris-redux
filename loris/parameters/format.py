from loris.exceptions.request_exception import RequestException
from loris.exceptions.syntax_exception import SyntaxException
from loris.exceptions.feature_not_enabled_exception import FeatureNotEnabledException
from loris.parameters.api import AbstractParameter

JPG = 'jpg'
PNG = 'png'
WEBP = 'webp'
ALL = (JPG, PNG, WEBP)

class FormatParameter(AbstractParameter):

    def __init__(self, uri_slice, enabled_features, formats_available):
        super().__init__(uri_slice, enabled_features)
        self.formats_available = formats_available
        self._canonical = uri_slice
        self._run_checks()

    @property
    def canonical(self):
        return self._canonical

    def _run_checks(self):
        if self.canonical not in ALL:
            msg = '{0} is not a recognized format'.format(self.canonical)
            raise SyntaxException(msg)
        if self.canonical == PNG and PNG not in self.enabled_features:
            raise FeatureNotEnabledException(PNG)
        if self.canonical not in self.formats_available:
            msg = '{0} is not an available format'.format(self.canonical)
            raise RequestException(msg)
