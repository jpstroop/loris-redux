from loris.constants import ALL_QUALITIES
from loris.constants import QUALITY_COLOR
from loris.constants import KEYWORD_DEFAULT
from loris.constants import QUALITY_GRAY
from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import RequestException
from loris.exceptions import SyntaxException
from loris.parameters.api import AbstractParameter

class QualityParameter(AbstractParameter):
    # TODO: leave room for compression extensions like dithered, default_low

    def __init__(self, uri_slice, enabled_features, info):
        super().__init__(uri_slice, enabled_features)
        self.qualities_available = info.extra_qualities + (KEYWORD_DEFAULT,)
        self.image_is_color = QUALITY_COLOR in self.qualities_available
        self._run_checks()

    @property
    def canonical(self):
        if self._canonical is None:
            is_default = any((
                self.image_is_color and self.uri_slice == QUALITY_COLOR,
                not self.image_is_color and self.uri_slice == QUALITY_GRAY,
                self.uri_slice == KEYWORD_DEFAULT
            ))
            self._canonical = KEYWORD_DEFAULT if is_default else self.uri_slice # TODO: constants!
        return self._canonical

    def _run_checks(self):
        self._is_recognizable()
        self._check_quality_available()
        self._check_feature_enabled()

    def _is_recognizable(self):
        if self.uri_slice not in ALL_QUALITIES:
            msg = f'Value "{self.uri_slice}" for quality is not recognized'
            raise SyntaxException(msg)

    def _check_quality_available(self):
        if self.uri_slice not in self.qualities_available:
            msg = f'{self.uri_slice} quality is not available for this image'
            raise RequestException(msg)

    def _check_feature_enabled(self):
        if self.uri_slice == KEYWORD_DEFAULT:
            return
        if self.uri_slice not in self.enabled_features:
            raise FeatureNotEnabledException(self.uri_slice)
