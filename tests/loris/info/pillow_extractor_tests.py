from loris.helpers.compliance import Compliance
from loris.info.abstract_extractor import COLOR_QUALITIES
from loris.info.abstract_extractor import GRAY_QUALITIES
from loris.info.pillow_extractor import PillowExtractor
import pytest

HTTP_ID = 'https://example.edu/images/1234'

def init_and_extract(path, compliance, app_configs):
    return PillowExtractor(compliance, app_configs).extract(path, HTTP_ID)

class TestPillowExtractor(object):

    def test__level_zero_tiles_wide(self):
        tiles = PillowExtractor._level_zero_tiles(7201, 3893, 1024, 1024)
        only_entry = tiles[0]
        assert only_entry['width'] == 1024
        assert only_entry.get('height') is None
        assert only_entry['scaleFactors'] == [1, 2, 4]

    def test__level_zero_tiles_tall(self):
        tiles = PillowExtractor._level_zero_tiles(2000, 11003, 512, 512)
        only_entry = tiles[0]
        assert only_entry['width'] == 512
        assert only_entry.get('height') is None
        assert only_entry['scaleFactors'] == [1, 2, 4, 8, 16]

    def test__level_zero_sizes(self):
        sizes = PillowExtractor._level_zero_sizes(4, 7201, 3664)
        assert sizes[0]['width'] == 1801
        assert sizes[0]['height'] == 916
        assert sizes[1]['width'] == 901
        assert sizes[1]['height'] == 458
        assert sizes[2]['width'] == 451
        assert sizes[2]['height'] == 229
        assert sizes[3]['width'] == 226
        assert sizes[3]['height'] == 115
        assert sizes[4]['width'] == 113
        assert sizes[4]['height'] == 58
        assert sizes[5]['width'] == 57
        assert sizes[5]['height'] == 29
        assert sizes[6]['width'] == 29
        assert sizes[6]['height'] == 15
        assert sizes[7]['width'] == 15
        assert sizes[7]['height'] == 8
        assert sizes[8]['width'] == 8
        assert sizes[8]['height'] == 4
        assert sizes[9]['width'] == 4
        assert sizes[9]['height'] == 2
        assert sizes[10]['width'] == 2
        assert sizes[10]['height'] == 1
        with pytest.raises(IndexError):
            _ = sizes[11]

    def test_wh_color_jpg(self, compliance_2, color_jpg, app_configs):
        info = init_and_extract(color_jpg, compliance_2, app_configs)
        assert info.width == 200
        assert info.height == 279


    def test_wh_color_png(self, compliance_2, color_png, app_configs):
        info = init_and_extract(color_png, compliance_2, app_configs)
        assert info.width == 200
        assert info.height == 250

    def test_color_jpg_qualities(self, compliance_2, color_jpg, app_configs):
        info = init_and_extract(color_jpg, compliance_2, app_configs)
        assert info.profile[1]['qualities'] == COLOR_QUALITIES

    def test_color_png_qualities(self, compliance_2, color_png, app_configs):
        info = init_and_extract(color_png, compliance_2, app_configs)
        assert info.profile[1]['qualities'] == COLOR_QUALITIES

    def test_gray_jpg_qualities(self, compliance_2, gray_jpg, app_configs):
        info = init_and_extract(gray_jpg, compliance_2, app_configs)
        assert info.profile[1]['qualities'] == GRAY_QUALITIES

    def test_gray_png_qualities(self, compliance_2, gray_png, app_configs):
        info = init_and_extract(gray_png, compliance_2, app_configs)
        assert info.profile[1]['qualities'] == GRAY_QUALITIES

    def test_sizes_color_jpg(self, compliance_0, color_jpg, app_configs):
        # so that tiles are smaller than the full test image:
        app_configs['scale_factors']['other_formats']['tile_width'] = 64
        app_configs['scale_factors']['other_formats']['tile_height'] = 64
        info = init_and_extract(color_jpg, compliance_0, app_configs)
        assert info.sizes[0] == {"height": 279, "width": 200}
        assert info.sizes[1] == {"height": 35, "width": 25}
        assert info.sizes[-1] == {"height": 2, "width": 1}

    def test_sizes_when_tile_is_larger_than_image(self, compliance_0, color_jpg, app_configs):
        # Default settings + test fixture raise this case
        info = init_and_extract(color_jpg, compliance_0, app_configs)
        assert info.sizes[0] == {"height": 279, "width": 200}
        assert info.sizes[1] == {"height": 140, "width": 100}
        assert info.sizes[2] == {"height": 70, "width": 50}
        assert info.sizes[3] == {"height": 35, "width": 25}
        assert info.sizes[-1] == {"height": 2, "width": 1}

    def test_profile_includes_max_area(self, compliance_2, color_jpg, app_configs):
        info = init_and_extract(color_jpg, compliance_2, app_configs)
        assert info.profile[1]['maxArea'] == 16000000

    def test_profile_includes_max_width(self, compliance_2, color_jpg, app_configs):
        app_configs['max_width'] = 7200
        info = init_and_extract(color_jpg, compliance_2, app_configs)
        assert info.profile[1]['maxWidth'] == 7200

    def test_profile_includes_max_width(self, compliance_2, color_jpg, app_configs):
        app_configs['max_height'] = 5000
        info = init_and_extract(color_jpg, compliance_2, app_configs)
        assert info.profile[1]['maxHeight'] == 5000

    def test_sizes_always_includes_full_or_max(self, compliance_0, color_jpg, app_configs):
        app_configs['scale_factors']['other_formats']['enabled'] = False
        app_configs['max_area'] = None
        app_configs['max_width'] = None
        app_configs['max_height'] = None
        info = init_and_extract(color_jpg, compliance_0, app_configs)
        assert info.sizes[0] == {"height": 279, "width": 200}
        with pytest.raises(IndexError):
            _ = info.sizes[1]
