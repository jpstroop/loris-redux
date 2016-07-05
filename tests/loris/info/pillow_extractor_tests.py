from loris.helpers.compliance import Compliance
from loris.info.abstract_extractor import COLOR_QUALITIES
from loris.info.abstract_extractor import GRAY_QUALITIES
from loris.info.pillow_extractor import PillowExtractor
from unittest.mock import MagicMock
import pytest

@pytest.fixture()
def compliance_all(everything_enabled_json):
    return Compliance(everything_enabled_json)

@pytest.fixture()
def compliance0():
    m = MagicMock(level=0, compliance_uri='http://iiif.io/api/image/2/level0.json')
    m.to_profile = lambda **kwargs : {} # We don't need to test this here, just need to be serializable.
    return m

HTTP_ID = 'https://example.edu/images/1234'

def init_and_extract(path, compliance, app_configs):
    return PillowExtractor(compliance, app_configs).extract(path, HTTP_ID)

class TestPillowExtractor(object):

    def test_wh_color_jpg(self, compliance_all, color_jpg, app_configs):
        info = init_and_extract(color_jpg, compliance_all, app_configs)
        assert info.width == 200
        assert info.height == 279

    def test_wh_color_png(self, compliance_all, color_png, app_configs):
        info = init_and_extract(color_png, compliance_all, app_configs)
        assert info.width == 200
        assert info.height == 250

    def test_color_jpg_qualities(self, compliance_all, color_jpg, app_configs):
        info = init_and_extract(color_jpg, compliance_all, app_configs)
        assert info.profile[1]['qualities'] == COLOR_QUALITIES

    def test_color_png_qualities(self, compliance_all, color_png, app_configs):
        info = init_and_extract(color_png, compliance_all, app_configs)
        assert info.profile[1]['qualities'] == COLOR_QUALITIES

    def test_gray_jpg_qualities(self, compliance_all, gray_jpg, app_configs):
        info = init_and_extract(gray_jpg, compliance_all, app_configs)
        assert info.profile[1]['qualities'] == GRAY_QUALITIES

    def test_gray_png_qualities(self, compliance_all, gray_png, app_configs):
        info = init_and_extract(gray_png, compliance_all, app_configs)
        assert info.profile[1]['qualities'] == GRAY_QUALITIES

    def test_sizes_color_jpg(self, compliance0, color_jpg, app_configs):
        # so that tiles are smaller than the full test image:
        app_configs['scale_factors']['other_formats']['tile_width'] = 64
        app_configs['scale_factors']['other_formats']['tile_height'] = 64
        info = init_and_extract(color_jpg, compliance0, app_configs)
        assert info.sizes[0] == {"height": 279, "width": 200}
        assert info.sizes[1] == {"height": 35, "width": 25}
        assert info.sizes[-1] == {"height": 2, "width": 1}

    def test_sizes_when_tile_is_larger_than_image(self, compliance0, color_jpg, app_configs):
        # Default settings + test fixture raise this case
        info = init_and_extract(color_jpg, compliance0, app_configs)
        assert info.sizes[0] == {"height": 279, "width": 200}
        assert info.sizes[1] == {"height": 140, "width": 100}
        assert info.sizes[2] == {"height": 70, "width": 50}
        assert info.sizes[3] == {"height": 35, "width": 25}
        assert info.sizes[-1] == {"height": 2, "width": 1}

    def test_profile_includes_max_area(self, compliance_all, color_jpg, app_configs):
        info = init_and_extract(color_jpg, compliance_all, app_configs)
        assert info.profile[1]['maxArea'] == 16000000

    def test_profile_includes_max_width(self, compliance_all, color_jpg, app_configs):
        app_configs['max_width'] = 7200
        info = init_and_extract(color_jpg, compliance_all, app_configs)
        assert info.profile[1]['maxWidth'] == 7200

    def test_profile_includes_max_width(self, compliance_all, color_jpg, app_configs):
        app_configs['max_height'] = 5000
        info = init_and_extract(color_jpg, compliance_all, app_configs)
        assert info.profile[1]['maxHeight'] == 5000
