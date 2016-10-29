from loris.constants import ALL_QUALITIES
from loris.constants import COLOR
from loris.constants import DEFAULT
from loris.constants import GRAY
from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import RequestException
from loris.exceptions import SyntaxException
from loris.parameters.api import AbstractParameter

class QualityParameter(AbstractParameter):
    # TODO: leave room for compression extensions like dithered, default_low

    def __init__(self, uri_slice, enabled_features, info):
        super().__init__(uri_slice, enabled_features)
        self.qualities_available = info.profile[1]['qualities'] + (DEFAULT,)
        self.image_is_color = COLOR in self.qualities_available
        self._run_checks()

    @property
    def canonical(self):
        if self._canonical is None:
            is_default = any((
                self.image_is_color and self.uri_slice == COLOR,
                not self.image_is_color and self.uri_slice == GRAY,
                self.uri_slice == DEFAULT
            ))
            self._canonical = DEFAULT if is_default else self.uri_slice # TODO: constants!
        return self._canonical

    def _run_checks(self):
        self._is_recognizable()
        self._check_quality_available()
        self._check_feature_enabled()

    def _is_recognizable(self):
        if self.uri_slice not in ALL_QUALITIES:
            msg = 'Value "{0}" for quality is not recognized'
            raise SyntaxException(msg.format(self.uri_slice))

    def _check_quality_available(self):
        if self.uri_slice not in self.qualities_available:
            msg = '{0} quality is not available for this image'
            raise RequestException(msg.format(self.uri_slice))

    def _check_feature_enabled(self):
        if self.uri_slice == DEFAULT:
            return
        if self.uri_slice not in self.enabled_features:
            raise FeatureNotEnabledException(self.uri_slice)
