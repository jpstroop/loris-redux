from loris.helpers.compliance import Compliance
from loris.info.abstract_extractor import COLOR_QUALITIES
from loris.info.abstract_extractor import GRAY_QUALITIES
from loris.info.pillow_extractor import PillowExtractor
from unittest.mock import MagicMock
import pytest

@pytest.fixture()
def compliance_everything(everything_enabled_json):
    return Compliance(everything_enabled_json)

@pytest.fixture()
def compliance_0():
    m = MagicMock(level=0, compliance_uri='http://iiif.io/api/image/2/level0.json')
    m.to_profile = lambda include_color : {} # We don't need to test this here, just need to be serializable.
    return m

app_configs_with_tiles = {
    'scale_factors' : {
        'enabled': True,
        'tile_width': 64,
        'tile_height': 64
    }
}

HTTP_ID = 'https://example.edu/images/1234'

class TestPillowExtractor(object):

    def load_and_extract(self, path, compliance, app_configs=app_configs_with_tiles):
        ex = PillowExtractor(compliance, app_configs)
        return ex.extract(path, HTTP_ID)

    def test_wh_color_jpg(self, compliance_everything, color_jpg):
        info_data = self.load_and_extract(color_jpg, compliance_everything)
        assert info_data.width == 200
        assert info_data.height == 279

    def test_wh_color_png(self, compliance_everything, color_png):
        info_data = self.load_and_extract(color_png, compliance_everything)
        assert info_data.width == 200
        assert info_data.height == 250

    def test_color_jpg_qualities(self, compliance_everything, color_jpg):
        info_data = self.load_and_extract(color_jpg, compliance_everything)
        assert info_data.profile[1]['qualities'] == COLOR_QUALITIES

    def test_color_png_qualities(self, compliance_everything, color_png):
        info_data = self.load_and_extract(color_png, compliance_everything)
        assert info_data.profile[1]['qualities'] == COLOR_QUALITIES

    def test_gray_jpg_qualities(self, compliance_everything, gray_jpg):
        info_data = self.load_and_extract(gray_jpg, compliance_everything)
        assert info_data.profile[1]['qualities'] == GRAY_QUALITIES

    def test_gray_png_qualities(self, compliance_everything, gray_png):
        info_data = self.load_and_extract(gray_png, compliance_everything)
        assert info_data.profile[1]['qualities'] == GRAY_QUALITIES

    def test_sizes_color_jpg(self, compliance_0, color_jpg):
        info_data = self.load_and_extract(color_jpg, compliance_0, app_configs_with_tiles)
        d = info_data._to_dict()
        assert d['sizes'][0] == {"height": 279, "width": 200}
        assert d['sizes'][1] == {"height": 35, "width": 25}
        assert d['sizes'][-1] == {"height": 2, "width": 1}
