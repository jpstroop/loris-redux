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
    m.to_profile = lambda **kwargs : {} # We don't need to test this here, just need to be serializable.
    return m

# TODO: load these from the config file as a fixture so that we know tests &
# reality are in sync
default_app_configs =  {
    "server_uri": None,
    "max_area": 16000000,
    "max_width": None,
    "max_height": None,
    "scale_factors": {
        "jp2": { "encoded_only": False },
        "other_formats" : {
            "enabled": True,
            "tile_width": 1024,
            "tile_height": 1024
        }
    }
}

HTTP_ID = 'https://example.edu/images/1234'

def load_and_extract(path, compliance, app_configs=default_app_configs):
    ex = PillowExtractor(compliance, app_configs)
    return ex.extract(path, HTTP_ID)

class TestPillowExtractor(object):

    def test_wh_color_jpg(self, compliance_everything, color_jpg):
        info_data = load_and_extract(color_jpg, compliance_everything)
        assert info_data.width == 200
        assert info_data.height == 279

    def test_wh_color_png(self, compliance_everything, color_png):
        info_data = load_and_extract(color_png, compliance_everything)
        assert info_data.width == 200
        assert info_data.height == 250

    def test_color_jpg_qualities(self, compliance_everything, color_jpg):
        info_data = load_and_extract(color_jpg, compliance_everything)
        assert info_data.profile[1]['qualities'] == COLOR_QUALITIES

    def test_color_png_qualities(self, compliance_everything, color_png):
        info_data = load_and_extract(color_png, compliance_everything)
        assert info_data.profile[1]['qualities'] == COLOR_QUALITIES

    def test_gray_jpg_qualities(self, compliance_everything, gray_jpg):
        info_data = load_and_extract(gray_jpg, compliance_everything)
        assert info_data.profile[1]['qualities'] == GRAY_QUALITIES

    def test_gray_png_qualities(self, compliance_everything, gray_png):
        info_data = load_and_extract(gray_png, compliance_everything)
        assert info_data.profile[1]['qualities'] == GRAY_QUALITIES

    def test_sizes_color_jpg(self, compliance_0, color_jpg):
        configs =  {
            "server_uri": None,
            "max_area": 16000000,
            "max_width": None,
            "max_height": None,
            "scale_factors": {
                "jp2": { "encoded_only": False },
                "other_formats" : {
                    "enabled": True,
                    "tile_width": 64, # so that tiles are smaller than the full
                    "tile_height": 64 # test image
                }
            }
        }
        info_data = load_and_extract(color_jpg, compliance_0, app_configs=configs)
        d = info_data._to_dict()
        assert info_data.sizes[0] == {"height": 279, "width": 200}
        assert info_data.sizes[1] == {"height": 35, "width": 25}
        assert info_data.sizes[-1] == {"height": 2, "width": 1}

    def test_sizes_when_tile_is_larger_than_image(self, compliance_0, color_jpg):
        # Default settings + test fixture raise this case
        info_data = load_and_extract(color_jpg, compliance_0)
        assert info_data.sizes[0] == {"height": 279, "width": 200}
        assert info_data.sizes[1] == {"height": 140, "width": 100}
        assert info_data.sizes[2] == {"height": 70, "width": 50}
        assert info_data.sizes[3] == {"height": 35, "width": 25}
        assert info_data.sizes[-1] == {"height": 2, "width": 1}

    def test_profile_includes_max_area(self, compliance_everything, color_jpg):
        info_data = load_and_extract(color_jpg, compliance_everything)
        assert info_data.profile[1]['maxArea'] == 16000000

    def test_profile_includes_max_width(self, compliance_everything, color_jpg):
        configs =  {
            "server_uri": None,
            "max_area": None,
            "max_width": 7200,
            "max_height": None,
            "scale_factors": {
                "jp2": { "encoded_only": False },
                "other_formats" : {
                    "enabled": True,
                    "tile_width": 1024, # so that tiles are smaller than the full
                    "tile_height": 1024 # test image
                }
            }
        }
        info_data = load_and_extract(color_jpg, compliance_everything, app_configs=configs)
        assert info_data.profile[1]['maxWidth'] == 7200

    def test_profile_includes_max_width(self, compliance_everything, color_jpg):
        configs =  {
            "server_uri": None,
            "max_area": None,
            "max_width": None,
            "max_height": 5000,
            "scale_factors": {
                "jp2": { "encoded_only": False },
                "other_formats" : {
                    "enabled": True,
                    "tile_width": 1024, # so that tiles are smaller than the full
                    "tile_height": 1024 # test image
                }
            }
        }
        info_data = load_and_extract(color_jpg, compliance_everything, app_configs=configs)
        assert info_data.profile[1]['maxHeight'] == 5000
