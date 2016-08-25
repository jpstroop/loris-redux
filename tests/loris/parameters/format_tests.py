from loris.exceptions import SyntaxException
from loris.exceptions import FeatureNotEnabledException
from loris.parameters.format import FormatParameter

import pytest

class TestFormatParameter(object):

    def test_png_with_all_enabled(self):
        uri_slice = 'png'
        enabled_features = ('png', 'webp')
        formats_available = ('jpg', 'png', 'webp')
        fp = FormatParameter(uri_slice, enabled_features, formats_available)
        assert fp.canonical == 'png'

    def test_webp_with_all_enabled(self):
        uri_slice = 'webp'
        enabled_features = ('png', 'webp')
        formats_available = ('jpg', 'png', 'webp')
        fp = FormatParameter(uri_slice, enabled_features, formats_available)
        assert fp.canonical == 'webp'

    def test_jpg_with_all_enabled(self):
        uri_slice = 'jpg'
        enabled_features = ('png', 'webp')
        formats_available = ('jpg', 'png', 'webp')
        fp = FormatParameter(uri_slice, enabled_features, formats_available)
        assert fp.canonical == 'jpg'

    def test_jpeg_with_none_enabled(self):
        uri_slice = 'jpg'
        enabled_features = ()
        formats_available = ('jpg', 'png', 'webp')
        fp = FormatParameter(uri_slice, enabled_features, formats_available)
        assert fp.canonical == 'jpg'

    def test_png_with_none_enabled_raises(self):
        uri_slice = 'png'
        enabled_features = ()
        formats_available = ('jpg', 'png', 'webp')
        with pytest.raises(FeatureNotEnabledException) as fe:
            FormatParameter(uri_slice, enabled_features, formats_available)
        assert "Server does not support the 'png' feature." in fe.value.message

    def test_unrecognized_raises(self):
        uri_slice = 'wtf'
        enabled_features = ('jpg', 'png')
        formats_available = ('jpg', 'png', 'webp')
        with pytest.raises(SyntaxException) as se:
            FormatParameter(uri_slice, enabled_features, formats_available)
        assert 'wtf is not a recognized format' == se.value.message
