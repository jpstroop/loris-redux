import re

from loris.constants import FEATURE_ROTATION_ARBITRARY
from loris.constants import FEATURE_ROTATION_BY_90S
from loris.constants import FEATURE_ROTATION_MIRRORING
from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import RequestException
from loris.exceptions import SyntaxException
from loris.parameters.api import AbstractParameter

REGEX = re.compile(r'^!?\d+(?:\.\d+)?$')

class RotationParameter(AbstractParameter):

    def __init__(self, uri_slice, enabled_features):
        super().__init__(uri_slice, enabled_features)
        if not REGEX.match(uri_slice):
            msg = f'Could not parse region request ({uri_slice})'
            raise SyntaxException(msg)
        self.mirror = self.uri_slice[0] == '!'
        self._rotation = None
        self._run_checks()

    @property
    def rotation(self):
        # raises SyntaxException
        if self._rotation is None:
            s = self.uri_slice[1:] if self.mirror else self.uri_slice
            self._rotation = float(s)
        return self._rotation

    @property
    def canonical(self):
        if self._canonical is None:
            if self.mirror:
                self._canonical = f'!{self.rotation:g}'
            else:
                self._canonical = f'{self.rotation:g}'
        return self._canonical

    def _run_checks(self):
        self._check_range()
        self._check_mirroring()
        self._check_rotation()

    def _check_range(self):
        if not 0.0 <= self.rotation <= 360.0:
            msg = f'Rotation must be between 0 and 360 ({self.rotation})'
            raise RequestException(msg)

    def _check_mirroring(self):
        if self.mirror and FEATURE_ROTATION_MIRRORING not in self.enabled_features:
            raise FeatureNotEnabledException(FEATURE_ROTATION_MIRRORING)

    def _check_rotation(self):
        if self.rotation == 0.0:
            return
        if self.rotation % 90 == 0.0 and FEATURE_ROTATION_BY_90S not in self.enabled_features:
            raise FeatureNotEnabledException(FEATURE_ROTATION_BY_90S)
        if self.rotation % 90 != 0.0 and FEATURE_ROTATION_ARBITRARY not in self.enabled_features:
            raise FeatureNotEnabledException(FEATURE_ROTATION_ARBITRARY)
