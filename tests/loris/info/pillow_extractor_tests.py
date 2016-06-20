from loris.helpers.compliance import Compliance
from loris.info.extract_api import COLOR_QUALITIES
from loris.info.extract_api import GRAY_QUALITIES
from loris.info.pillow_extractor import PillowExtractor
import pytest

@pytest.fixture()
def compliance_everything(everything_enabled_json):
    return Compliance(everything_enabled_json)

HTTP_ID = 'https://example.edu/images/1234'

class TestPillowExtractor(object):

    def load_and_extract(self, path, compliance):
        app_configs = {}
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
