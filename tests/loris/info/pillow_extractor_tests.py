from loris.compliance import Compliance
from loris.constants import COLOR_QUALITIES
from loris.constants import GRAY_QUALITIES
from loris.info.pillow_extractor import PillowExtractor
from loris.info.structs.size import Size
from loris.info.structs.tile import Tile
import pytest

HTTP_ID = 'https://example.edu/images/1234'

def init_and_extract(path, compliance, app_configs):
    return PillowExtractor(compliance, app_configs).extract(path, HTTP_ID)

class TestPillowExtractor(object):

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
        app_configs['sizes_and_tiles']['other_formats']['tile_width'] = 64
        app_configs['sizes_and_tiles']['other_formats']['tile_height'] = 64
        info = init_and_extract(color_jpg, compliance_0, app_configs)
        assert info.sizes[0] == Size(200, 279)

    def test_sizes_when_tile_is_larger_than_image(self, compliance_0, color_jpg, app_configs):
        # Default settings + test fixture raise this case
        info = init_and_extract(color_jpg, compliance_0, app_configs)
        assert info.sizes[0] == Size(200, 279)
        assert info.sizes[1] == Size(100, 140)

    def test_scale_factors(self, compliance_2, app_configs):
        pe = PillowExtractor(compliance_2, app_configs)
        assert pe._scale_factors(6000,8000) == [1, 2, 4, 8, 16, 32, 64]

    def test_tiles_and_sizes_reported_with_higher_compliance(self, compliance_2, region_test_jpg, app_configs):
        info = init_and_extract(region_test_jpg, compliance_2, app_configs)
        assert info.tiles[0].scale_factors == (1, 2, 4)
        assert info.sizes[0].width == 3464
        assert info.sizes[0].height == 4619
        assert info.sizes[1].width == 3000
        assert info.sizes[1].height == 4000
        assert info.sizes[2].width == 1500
        assert info.sizes[2].height == 2000
        assert info.sizes[3].width == 750
        assert info.sizes[3].height == 1000
        assert info.sizes[4].width == 375
        assert info.sizes[4].height == 500
        assert info.sizes[5].width == 188
        assert info.sizes[5].height == 250
        assert info.sizes[6].width == 94
        assert info.sizes[6].height == 125

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
        app_configs['sizes_and_tiles']['other_formats']['enabled'] = False
        app_configs['max_area'] = None
        app_configs['max_width'] = None
        app_configs['max_height'] = None
        info = init_and_extract(color_jpg, compliance_0, app_configs)
        assert info.sizes[0] == Size(200, 279)
        with pytest.raises(IndexError):
            _ = info.sizes[1]
