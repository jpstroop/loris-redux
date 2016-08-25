from loris.exceptions import SyntaxException
from loris.exceptions import FeatureNotEnabledException
from loris.parameters.quality import QualityParameter

import pytest

class TestQualityParameter(object):

    def test_canonical_color_with_color(self):
        uri_slice = 'color'
        enabled_features = ('color', 'bitonal', 'gray')
        qualities_available = ('color', 'bitonal', 'gray')
        qp = QualityParameter(uri_slice, enabled_features, qualities_available)
        assert qp.canonical == 'default'

    def test_canonical_gray_with_color(self):
        uri_slice = 'gray'
        enabled_features = ('color', 'bitonal', 'gray')
        qualities_available = ('color', 'bitonal', 'gray')
        qp = QualityParameter(uri_slice, enabled_features, qualities_available)
        assert qp.canonical == 'gray'

    def test_canonical_gray_with_gray(self):
        uri_slice = 'gray'
        enabled_features = ('color', 'bitonal', 'gray')
        qualities_available = ('bitonal', 'gray')
        qp = QualityParameter(uri_slice, enabled_features, qualities_available)
        assert qp.canonical == 'default'

    def test_gray_raises_if_not_enabled(self):
        uri_slice = 'gray'
        enabled_features = ('color', 'bitonal')
        qualities_available = ('bitonal', 'gray')
        with pytest.raises(FeatureNotEnabledException) as fe:
            QualityParameter(uri_slice, enabled_features, qualities_available)
        assert "not support the 'gray'" in fe.value.message

    def test_unrecognizable_raises(self):
        uri_slice = 'foo'
        enabled_features = ('color', 'bitonal', 'gray')
        qualities_available = ('color', 'bitonal', 'gray')
        with pytest.raises(SyntaxException) as se:
            QualityParameter(uri_slice, enabled_features, qualities_available)
        assert 'Value "foo" for quality is not recognized' == se.value.message

    @pytest.mark.skip(reason='test not written')
    def test_bitonal_nodither_extension(self):
        raise NotImplementedError
