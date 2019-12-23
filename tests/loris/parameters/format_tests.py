from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import SyntaxException
from loris.parameters.format import FormatParameter
from unittest.mock import Mock
import pytest


class TestFormatParameter(object):
    def mock_info(self, formats_available):
        return Mock(extra_formats=formats_available)

    def test_png_with_all_enabled(self):
        uri_slice = "png"
        enabled_features = ("png", "webp")
        info = self.mock_info(("jpg", "png", "webp"))
        fp = FormatParameter(uri_slice, enabled_features, info)
        assert fp.canonical == "png"

    def test_webp_with_all_enabled(self):
        uri_slice = "webp"
        enabled_features = ("png", "webp")
        info = self.mock_info(("jpg", "png", "webp"))
        fp = FormatParameter(uri_slice, enabled_features, info)
        assert fp.canonical == "webp"

    def test_jpg_with_all_enabled(self):
        uri_slice = "jpg"
        enabled_features = ("png", "webp")
        info = self.mock_info(("jpg", "png", "webp"))
        fp = FormatParameter(uri_slice, enabled_features, info)
        assert fp.canonical == "jpg"

    def test_jpeg_with_none_enabled(self):
        uri_slice = "jpg"
        enabled_features = ()
        info = self.mock_info(("jpg", "png", "webp"))
        fp = FormatParameter(uri_slice, enabled_features, info)
        assert fp.canonical == "jpg"

    def test_png_with_none_enabled_raises(self):
        uri_slice = "png"
        enabled_features = ()
        info = self.mock_info(("jpg", "png", "webp"))
        with pytest.raises(FeatureNotEnabledException) as fe:
            FormatParameter(uri_slice, enabled_features, info)
        assert "Server does not support the 'png' feature." in fe.value.message

    def test_unrecognized_raises(self):
        uri_slice = "wtf"
        enabled_features = ("jpg", "png")
        info = self.mock_info(("jpg", "png", "webp"))
        with pytest.raises(SyntaxException) as se:
            FormatParameter(uri_slice, enabled_features, info)
        assert "wtf is not a recognized format" == se.value.message
