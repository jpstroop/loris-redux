from loris.exceptions.request_exception import RequestException
from loris.exceptions.syntax_exception import SyntaxException
from loris.exceptions.feature_not_enabled_exception import FeatureNotEnabledException
from loris.parameters.api import AbstractParameter
import re

BY_90S = 'rotationBy90s'
ARBITRARY = 'rotationArbitrary'
MIRRORING = 'mirroring'
REGEX = re.compile(r'^!?\d+(?:\.\d+)?$')

class RotationParameter(AbstractParameter):

    def __init__(self, uri_slice, enabled_features):
        super().__init__(uri_slice, enabled_features)
        if not REGEX.match(uri_slice):
            msg = 'Could not parse region request ({0})'.format(uri_slice)
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
                self._canonical = '!{:g}'.format(self.rotation)
            else:
                self._canonical = '{:g}'.format(self.rotation)
        return self._canonical

    def _run_checks(self):
        self._check_range()
        self._check_mirroring()
        self._check_rotation()

    def _check_range(self):
        if not 0.0 <= self.rotation <= 360.0:
            msg = 'Rotation must be between 0 and 360 ({0})'.format(self.rotation)
            raise RequestException(msg)

    def _check_mirroring(self):
        if self.mirror and MIRRORING not in self.enabled_features:
            raise FeatureNotEnabledException(MIRRORING)

    def _check_rotation(self):
        if self.rotation == 0.0:
            return
        if self.rotation % 90 == 0.0 and BY_90S not in self.enabled_features:
            raise FeatureNotEnabledException(BY_90S)
        if self.rotation % 90 != 0.0 and ARBITRARY not in self.enabled_features:
            raise FeatureNotEnabledException(ARBITRARY)
