from loris.exceptions import SyntaxException
from loris.exceptions import FeatureNotEnabledException
from loris.parameters.quality import QualityParameter
from unittest.mock import Mock

import pytest

class TestQualityParameter(object):

    def mock_info(self, qualities_available):
        return Mock(extra_qualities=qualities_available)

    def test_canonical_color_with_color(self):
        uri_slice = 'color'
        enabled_features = ('color', 'bitonal', 'gray')
        info = self.mock_info(('color', 'bitonal', 'gray'))
        qp = QualityParameter(uri_slice, enabled_features, info)
        assert qp.canonical == 'default'

    def test_canonical_gray_with_color(self):
        uri_slice = 'gray'
        enabled_features = ('color', 'bitonal', 'gray')
        info = self.mock_info(('color', 'bitonal', 'gray'))
        qp = QualityParameter(uri_slice, enabled_features, info)
        assert qp.canonical == 'gray'

    def test_canonical_gray_with_gray(self):
        uri_slice = 'gray'
        enabled_features = ('color', 'bitonal', 'gray')
        info = self.mock_info(('bitonal', 'gray'))
        qp = QualityParameter(uri_slice, enabled_features, info)
        assert qp.canonical == 'default'

    def test_gray_raises_if_not_enabled(self):
        uri_slice = 'gray'
        enabled_features = ('color', 'bitonal')
        info = self.mock_info(('bitonal', 'gray'))
        with pytest.raises(FeatureNotEnabledException) as fe:
            QualityParameter(uri_slice, enabled_features, info)
        assert "not support the 'gray'" in fe.value.message

    def test_unrecognizable_raises(self):
        uri_slice = 'foo'
        enabled_features = ('color', 'bitonal', 'gray')
        info = self.mock_info(('color', 'bitonal', 'gray'))
        with pytest.raises(SyntaxException) as se:
            QualityParameter(uri_slice, enabled_features, info)
        assert 'Value "foo" for quality is not recognized' == se.value.message

    @pytest.mark.skip(reason='test not written')
    def test_bitonal_nodither_extension(self):
        raise NotImplementedError
