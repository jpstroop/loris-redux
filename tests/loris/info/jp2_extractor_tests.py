from loris.compliance import Compliance
from loris.constants import COLOR_QUALITIES
from loris.constants import GRAY_QUALITIES
from loris.info.jp2_extractor import Jp2Parser
from loris.info.jp2_extractor import Jp2Extractor
import pytest

HTTP_ID = 'https://example.edu/images/1234'

def init_and_extract(path, compliance, app_configs):
    return Jp2Extractor(compliance, app_configs).extract(path, HTTP_ID)

class TestJp2Extractor(object):

    def test_wh(self, compliance_2, tiled_jp2, app_configs):
        info = init_and_extract(tiled_jp2, compliance_2, app_configs)
        assert info.width == 5906
        assert info.height == 7200

    def test_precinct_tiles(self, compliance_2, precincts_jp2, app_configs):
        info = init_and_extract(precincts_jp2, compliance_2, app_configs)
        assert info.tiles[0].width == 512
        assert info.tiles[0].scale_factors == [1]
        assert info.tiles[1].width == 256
        assert info.tiles[1].scale_factors == [2]
        assert info.tiles[2].width == 128
        assert info.tiles[2].scale_factors == [4, 8, 16, 32]

    def test_tiled_tiles(self, compliance_2, tiled_jp2, app_configs):
        info = init_and_extract(tiled_jp2, compliance_2, app_configs)
        assert info.tiles[0].width == 256
        assert info.tiles[0].scale_factors == [1, 2, 4, 8, 16, 32]

    def test_region_test_img_tiles(self, compliance_2, region_test_jp2, app_configs):
        info = init_and_extract(region_test_jp2, compliance_2, app_configs)
        assert info.tiles[0].width == 1024

    def test_sizes_no_max(self, compliance_2, tiled_jp2, app_configs):
        app_configs['max_area'] = None
        info = init_and_extract(tiled_jp2, compliance_2, app_configs)
        assert info.sizes[0].width == 5906
        assert info.sizes[0].height == 7200
        assert info.sizes[1].width == 2953
        assert info.sizes[1].height == 3600
        assert info.sizes[2].width == 1477
        assert info.sizes[2].height == 1800
        assert info.sizes[3].width == 739
        assert info.sizes[3].height == 900
        assert info.sizes[4].width == 370
        assert info.sizes[4].height == 450
        assert info.sizes[5].width == 185
        assert info.sizes[5].height == 225

    def test_profile_with_color(self, compliance_2, tiled_jp2, app_configs):
        info = init_and_extract(tiled_jp2, compliance_2, app_configs)
        assert info.profile[1]['qualities'] == COLOR_QUALITIES

    def test_profile_with_gray(self, compliance_2, gray_jp2, app_configs):
        info = init_and_extract(gray_jp2, compliance_2, app_configs)
        assert info.profile[1]['qualities'] == GRAY_QUALITIES

    def test_sizes_respects_max(self, compliance_2, tiled_jp2, app_configs):
        info = init_and_extract(tiled_jp2, compliance_2, app_configs)
        assert info.sizes[0].width == 3623
        assert info.sizes[0].height == 4417
        assert info.sizes[1].width == 2953
        assert info.sizes[1].height == 3600
        assert info.sizes[2].width == 1477
        assert info.sizes[2].height == 1800
        assert info.sizes[3].width == 739
        assert info.sizes[3].height == 900
        assert info.sizes[4].width == 370
        assert info.sizes[4].height == 450
        assert info.sizes[5].width == 185
        assert info.sizes[5].height == 225

    def test_profile_includes_max_area(self, compliance_2, tiled_jp2, app_configs):
        info = init_and_extract(tiled_jp2, compliance_2, app_configs)
        assert info.profile[1]['maxArea'] == 16000000

    def test_profile_includes_max_width(self, compliance_2, tiled_jp2, app_configs):
        app_configs['max_area'] = None
        app_configs['max_width'] = 4000
        info = init_and_extract(tiled_jp2, compliance_2, app_configs)
        assert info.profile[1]['maxWidth'] == 4000

    def test_profile_includes_max_height(self, compliance_2, tiled_jp2, app_configs):
        app_configs['max_area'] = None
        app_configs['max_height'] = 4001
        info = init_and_extract(tiled_jp2, compliance_2, app_configs)
        assert info.profile[1]['maxHeight'] == 4001

    def test_wh_in_sizes_l0_when_no_maxes(self, compliance_0, tiled_jp2, app_configs):
        app_configs['scale_factors']['jp2']['encoded_only'] = False
        app_configs['max_area'] = None
        app_configs['max_width'] = None
        app_configs['max_height'] = None
        info = init_and_extract(tiled_jp2, compliance_0, app_configs)
        assert info.sizes[0].width == 5906
        assert info.sizes[0].height == 7200
        with pytest.raises(IndexError):
            _ = info.sizes[1]

    def test_max_size_included_in_sizes_at_l0(self, compliance_0, tiled_jp2, app_configs):
        info = init_and_extract(tiled_jp2, compliance_0, app_configs)
        assert info.sizes[0].width == 3623
        assert info.sizes[0].height == 4417
        with pytest.raises(IndexError):
            _ = info.sizes[1]

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

    def test_tiles_for_region_test_jp2(self, region_test_jp2):
        info = Jp2Parser(region_test_jp2).metadata
        assert info['tile_width'] == 1024
        assert info['tile_height'] == 1024

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
        assert info['precincts'][0] == (512, 512)
        assert info['precincts'][1] == (256, 256)
        assert info['precincts'][2] == (128, 128)
        assert info['precincts'][3] == (128, 128)
        assert info['precincts'][4] == (128, 128)
        assert info['precincts'][5] == (128, 128)

    def test_no_precincts(self, tiled_jp2):
        info = Jp2Parser(tiled_jp2).metadata
        assert 'precincts' not in info
