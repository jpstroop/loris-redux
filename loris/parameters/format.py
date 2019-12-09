from loris.constants import ALL_OUTPUT_FORMATS
from loris.constants import JPG
from loris.constants import PNG
from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import RequestException
from loris.exceptions import SyntaxException
from loris.parameters.api import AbstractParameter

class FormatParameter(AbstractParameter):

    def __init__(self, uri_slice, enabled_features, info):
        super().__init__(uri_slice, enabled_features)
        self.formats_available = info.extra_formats
        self._canonical = uri_slice
        self._run_checks()

    @property
    def canonical(self):
        return self._canonical # TODO: should use the constants (PNG, JPG, etc)

    def _run_checks(self):
        if self.uri_slice == JPG:
            return
        if self.canonical not in ALL_OUTPUT_FORMATS:
            msg = f'{self.canonical} is not a recognized format'
            raise SyntaxException(msg)
        if self.canonical == PNG and PNG not in self.enabled_features:
            raise FeatureNotEnabledException(PNG)
        if self.canonical not in self.formats_available:
            msg = f'{self.canonical} is not an available format'
            raise RequestException(msg)
