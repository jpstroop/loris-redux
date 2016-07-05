from loris.helpers.compliance import Compliance
from loris.info.abstract_extractor import COLOR_QUALITIES
from loris.info.abstract_extractor import GRAY_QUALITIES
from loris.info.jp2_extractor import Jp2Parser
from loris.info.jp2_extractor import Jp2Extractor
from unittest.mock import MagicMock
import pytest

HTTP_ID = 'https://example.edu/images/1234'

@pytest.fixture()
def compliance_everything(everything_enabled_json):
    return Compliance(everything_enabled_json)

@pytest.fixture()
def compliance_0():
    m = MagicMock(level=0, compliance_uri='http://iiif.io/api/image/2/level0.json')
    m.to_profile = lambda **kwargs : {} # We don't need to test this here, just need to be serializable.
    return m

@pytest.fixture()
def compliance_1():
    m = MagicMock(level=1, compliance_uri='http://iiif.io/api/image/2/level1.json')
    m.to_profile = lambda **kwargs : {} # We don't need to test this here, just need to be serializable.
    return m

@pytest.fixture()
def compliance_2():
    m = MagicMock(level=2, compliance_uri='http://iiif.io/api/image/2/level2.json')
    # We don't need to test the server profile here, just needs to be serializable.
    m.to_profile = lambda **kwargs : {}
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

def load_and_extract(path, compliance, app_configs=default_app_configs):
    ex = Jp2Extractor(compliance, app_configs)
    return ex.extract(path, HTTP_ID)

class TestJp2Extractor(object):

    def test_wh(self, compliance_2, tiled_jp2):
        info_data = load_and_extract(tiled_jp2, compliance_2)
        # print('\n'+'*'*80)
        # print(info_data._to_dict().keys())
        # print('*'*80)
        assert info_data.width == 5906
        assert info_data.height == 7200

    def test_precinct_tiles(self, compliance_2, precincts_jp2):
        info_data = load_and_extract(precincts_jp2, compliance_2)
        assert info_data.tiles[0]['width'] == 512
        assert info_data.tiles[0]['scaleFactors'] == [1]
        assert info_data.tiles[1]['width'] == 256
        assert info_data.tiles[1]['scaleFactors'] == [2]
        assert info_data.tiles[2]['width'] == 128
        assert info_data.tiles[2]['scaleFactors'] == [4, 8, 16, 32]

    def test_tiled_tiles(self, compliance_2, tiled_jp2):
        info_data = load_and_extract(tiled_jp2, compliance_2)
        assert info_data.tiles[0]['width'] == 256
        assert info_data.tiles[0]['scaleFactors'] == [1, 2, 4, 8, 16, 32]

    def test_sizes_no_max(self, compliance_2, tiled_jp2):
        config =  {
            "server_uri": None,
            "max_area": None,
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
        info_data = load_and_extract(tiled_jp2, compliance_2, config)
        assert info_data.sizes[0]['width'] == 5906
        assert info_data.sizes[0]['height'] == 7200
        assert info_data.sizes[1]['width'] == 2953
        assert info_data.sizes[1]['height'] == 3600
        assert info_data.sizes[2]['width'] == 1477
        assert info_data.sizes[2]['height'] == 1800
        assert info_data.sizes[3]['width'] == 739
        assert info_data.sizes[3]['height'] == 900
        assert info_data.sizes[4]['width'] == 370
        assert info_data.sizes[4]['height'] == 450
        assert info_data.sizes[5]['width'] == 185
        assert info_data.sizes[5]['height'] == 225

    def test_profile_with_color(self, compliance_everything, tiled_jp2):
        info_data = load_and_extract(tiled_jp2, compliance_everything)
        assert info_data.profile[1]['qualities'] == COLOR_QUALITIES

    def test_profile_with_gray(self, compliance_everything, gray_jp2):
        info_data = load_and_extract(gray_jp2, compliance_everything)
        assert info_data.profile[1]['qualities'] == GRAY_QUALITIES

    def test_sizes_respects_max(self, compliance_2, tiled_jp2):
        info_data = load_and_extract(tiled_jp2, compliance_2)
        assert info_data.sizes[0]['width'] == 2953
        assert info_data.sizes[0]['height'] == 3600
        assert info_data.sizes[1]['width'] == 1477
        assert info_data.sizes[1]['height'] == 1800
        assert info_data.sizes[2]['width'] == 739
        assert info_data.sizes[2]['height'] == 900
        assert info_data.sizes[3]['width'] == 370
        assert info_data.sizes[3]['height'] == 450
        assert info_data.sizes[4]['width'] == 185
        assert info_data.sizes[4]['height'] == 225

    def test_profile_includes_max_area(self, compliance_everything, tiled_jp2):
        info_data = load_and_extract(tiled_jp2, compliance_everything)
        assert info_data.profile[1]['maxArea'] == 16000000

    def test_profile_includes_max_width(self, compliance_everything, tiled_jp2):
        config =  {
            "server_uri": None,
            "max_area": None,
            "max_width": 4000,
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
        info_data = load_and_extract(tiled_jp2, compliance_everything, config)
        assert info_data.profile[1]['maxWidth'] == 4000

    def test_profile_includes_max_height(self, compliance_everything, tiled_jp2):
        config =  {
            "server_uri": None,
            "max_area": None,
            "max_width": None,
            "max_height": 4000,
            "scale_factors": {
                "jp2": { "encoded_only": False },
                "other_formats" : {
                    "enabled": True,
                    "tile_width": 1024,
                    "tile_height": 1024
                }
            }
        }
        info_data = load_and_extract(tiled_jp2, compliance_everything, config)
        assert info_data.profile[1]['maxHeight'] == 4000

class TestJp2Parser(object):

    # We test just a few elements at a time so that tests can be run
    # independenty when debugging

    def test_wh(self, tiled_jp2):
        info = Jp2Parser(tiled_jp2).metadata
        assert info['image_width'] == 5906
        assert info['image_height'] == 7200

    def test_qualities_color_no_profile(self, tiled_jp2):
        info = Jp2Parser(tiled_jp2).metadata
        assert info['is_color']
        assert info.get('embedded_color_profile') is None

    def test_qualities_gray_no_profile(self, gray_jp2):
        info = Jp2Parser(gray_jp2).metadata
        assert not info['is_color']
        assert info.get('embedded_color_profile') is None

    def test_qualities_color_with_profile(self, color_profile_jp2):
        info = Jp2Parser(color_profile_jp2).metadata
        assert info['is_color']
        assert info.get('embedded_color_profile') is not None

    def test_tiles_for_tiled_jp2(self, tiled_jp2):
        info = Jp2Parser(tiled_jp2).metadata
        assert info['tile_width'] == 256
        assert info['tile_height'] == 256

    def test_levels(self, tiled_jp2):
        info = Jp2Parser(tiled_jp2).metadata
        assert info['levels'] == 6

    def test_tiles_for_precincts(self, precincts_jp2):
        # The fixture Jp2 was made with this command:
        # kdu_compress -i spec/fixtures/color.tif
        #   -o spec/fixtures/precincts.jp2
        #   Clevels=6
        #   Cprecincts="{512,512},{256,256},{128,128}"
        info = Jp2Parser(precincts_jp2).metadata
        #   {1: {'h': 512, 'w': 512}, 2: {'h': 256, 'w': 256}, 3: {'h': 128, 'w': 128}, 4: {'h': 128, 'w': 128}, 5: {'h': 128, 'w': 128}, 6: {'h': 128, 'w': 128}}
        assert info['precincts'][0] == (512, 512)
        assert info['precincts'][1] == (256, 256)
        assert info['precincts'][2] == (128, 128)
        assert info['precincts'][3] == (128, 128)
        assert info['precincts'][4] == (128, 128)
        assert info['precincts'][5] == (128, 128)


    def test_no_precincts(self, tiled_jp2):
        info = Jp2Parser(tiled_jp2).metadata
        assert 'precincts' not in info
