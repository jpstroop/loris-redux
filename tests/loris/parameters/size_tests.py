from loris.constants import KEYWORD_MAX
from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import RequestException
from loris.exceptions import SyntaxException
from loris.info.structs.size import Size
from loris.info.structs.tile import Tile
from loris.parameters.size import SizeParameter
from unittest.mock import Mock
import pytest


class TestSizeParameter(object):
    def mock_info(self, width, height, **kwargs):
        long_dim = max(width, height)
        short_dim = min(width, height)
        sizes = kwargs.get("sizes", [Size(width, height)])
        tiles = kwargs.get("tiles")
        max_area = kwargs.get("max_area")
        max_width = kwargs.get("max_width")
        max_height = kwargs.get("max_height")
        tiles = kwargs.get("tiles")
        kwargs = {
            "width": width,
            "height": height,
            "long_dim": long_dim,
            "short_dim": short_dim,
            "sizes": sizes,
            "tiles": tiles,
            "max_area": max_area,
            "max_width": max_width,
            "max_height": max_height,
        }
        return Mock(**kwargs)

    def mock_region(self, region_width, region_height):
        return Mock(pixel_w=region_width, pixel_h=region_height)

    def test__deduce_request_type_raises_syntax_exception(self):
        uri_slice = "wtf"
        info_data = self.mock_info(8000, 6001)
        features = ()
        region_param = self.mock_region(400, 300)
        with pytest.raises(SyntaxException) as se:
            _ = SizeParameter(uri_slice, features, info_data, region_param).request_type
        assert 'Size syntax "wtf" is not valid.' == se.value.message

    def test__init_max_size_ok(self):
        uri_slice = "max"
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(3456, 1234)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 3456
        assert sp.height == 1234
        assert sp.canonical is KEYWORD_MAX  # gets adjusted

    def test__init_max_over_size_w(self):
        uri_slice = "max"
        features = ()
        info_data = self.mock_info(8000, 6001, max_width=4000)
        region_param = self.mock_region(5000, 2000)  # 1000 wider than allowed
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 4000
        assert sp.height == 1600
        assert sp.canonical is KEYWORD_MAX

    def test__init_max_over_size_h(self):
        uri_slice = "max"
        features = ()
        info_data = self.mock_info(8000, 6000, max_height=4000)
        region_param = self.mock_region(5000, 4500)  # 500 higher than allowed
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 4444
        assert sp.height == 4000
        assert sp.canonical is KEYWORD_MAX

    def test__init_max_over_size_area(self):
        uri_slice = "max"
        features = ()
        max_area = 24000000
        info_data = self.mock_info(8000, 6000, max_area=24000000)
        region_param = self.mock_region(5000, 7000)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 4140
        assert sp.height == 5796
        assert (sp.height * sp.width) < max_area
        assert sp.canonical is KEYWORD_MAX

    def test__init_sizeByW(self):
        uri_slice = "1024,"
        features = "sizeByW"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2048, 2048)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 1024
        assert sp.height == 1024
        assert sp.canonical == "1024,1024"

    def test__check_if_supported_sizeByW_raises(self):
        uri_slice = "1024,"
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2048, 2048)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "not support the 'sizeByW'" in fe.value.message

    def test_max_as_sizeByW_adjusts_request_type(self):
        uri_slice = "1024,"
        features = "sizeByW"
        info_data = self.mock_info(8000, 6000, max_area=24000000)
        region_param = self.mock_region(1024, 1024)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 1024
        assert sp.height == 1024
        assert sp.request_type is KEYWORD_MAX
        assert sp.canonical == KEYWORD_MAX

    def test_full_as_sizeByW_still_raises(self):
        uri_slice = "1024,"
        features = ()
        info_data = self.mock_info(8000, 6000)
        region_param = self.mock_region(1024, 1024)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "not support the 'sizeByW'" in fe.value.message

    def test__init_sizeByH(self):
        uri_slice = ",1024"
        features = "sizeByH"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2048, 3072)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 683
        assert sp.height == 1024
        assert sp.canonical == "683,1024"

    @pytest.mark.skip(reason="test not written")
    def test_max_as_sizeByH_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="test not written")
    def test_max_as_sizeByH_still_raises(self):
        raise NotImplementedError

    def test__check_if_supported_sizeByH_raises(self):
        uri_slice = ",1024"
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2048, 3072)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "not support the 'sizeByH'" in fe.value.message

    def test__init_sizeByPct(self):
        uri_slice = "pct:20"
        features = "sizeByPct"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 400
        assert sp.height == 600
        assert sp.canonical == "400,600"

    def test__check_if_supported_sizeByPct_raises(self):
        uri_slice = "pct:20"
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2000, 3000)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "not support the 'sizeByPct'" in fe.value.message

    def test_pct_request_round_lt_0_to_1(self):
        uri_slice = "pct:0.01"
        features = "sizeByPct"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 1
        assert sp.height == 1
        assert sp.canonical == "1,1"

    def test_pct_0_raises(self):
        uri_slice = "pct:0"
        features = "sizeByPct"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2000, 3000)
        with pytest.raises(RequestException) as se:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "Size percentage must be greater than 0 (pct:0)." == se.value.message

    @pytest.mark.skip(reason="test not written")
    def test_full_as_sizeByPct_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="test not written")
    def test_full_as_sizeByPct_still_raises(self):
        raise NotImplementedError

    def test__init_sizeByConfinedWh_portrait(self):
        uri_slice = "!200,200"
        features = "sizeByConfinedWh"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 133
        assert sp.height == 200
        assert sp.canonical == "133,200"

    def test__init_sizeByConfinedWh_landscape(self):
        uri_slice = "!300,300"
        features = "sizeByConfinedWh"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2000, 1200)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 300
        assert sp.height == 180
        assert sp.canonical == "300,180"

    def test__check_if_supported_sizeByConfinedWh_raises(self):
        uri_slice = "!200,200"
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(2000, 3000)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "not support the 'sizeByConfinedWh'" in fe.value.message

    @pytest.mark.skip(reason="test not written")
    def test_full_as_sizeByConfinedWh_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="test not written")
    def test_full_as_sizeByConfinedWh_still_raises(self):
        raise NotImplementedError

    def test__init_sizeByWh(self):
        uri_slice = "400,300"
        features = "sizeByWh"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(8000, 6001)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 400
        assert sp.height == 300
        assert sp.canonical == "400,300"

    def test__check_if_supported_sizeByWh_raises(self):
        uri_slice = "400,300"
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(8000, 6001)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "not support the 'sizeByWh'" in fe.value.message

    @pytest.mark.skip(reason="test not written")
    def test_full_as_sizeByWh_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason="test not written")
    def test_full_as_sizeByWh_still_raises(self):
        raise NotImplementedError

    def test__sizeUpscaling_ok(self):  # This should raise now
        uri_slice = "400,300"
        features = ("sizeByWh", "sizeUpscaling")
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(399, 299)
        with pytest.raises(RequestException) as re:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "Image would be upsampled" in re.value.message

    def test_sizeUpscaling_raises(self):
        uri_slice = "^400,300"
        features = "sizeByWh"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(399, 299)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "not support the 'sizeUpscaling' feature" in fe.value.message

    def test_upscaling_ok_if_sizeUpscaling_enabled(self):
        uri_slice = "^400,300"
        features = ("sizeByWh", "sizeUpscaling")
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(399, 299)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.upscaling_requested
        assert sp.width == 400
        assert sp.height == 300
        assert sp.region_w == 399
        assert sp.region_h == 299

    def test_upscaling_ok_w_syntax(self):
        uri_slice = "^400,"
        features = ("sizeByW", "sizeUpscaling")
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(399, 299)
        SizeParameter(uri_slice, features, info_data, region_param)

    def test_upscaling_ok_h_syntax(self):
        uri_slice = "^,400"
        features = ("sizeByH", "sizeUpscaling")
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(399, 299)
        SizeParameter(uri_slice, features, info_data, region_param)

    def test_upscaling_ok_pct_syntax(self):
        uri_slice = "^pct:101"
        features = ("sizeByPct", "sizeUpscaling")
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(399, 299)
        SizeParameter(uri_slice, features, info_data, region_param)

    def test_upscaling_ok_pct_syntax(self):
        uri_slice = "^pct:101"
        features = ("sizeByPct", "sizeUpscaling")
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(399, 299)
        SizeParameter(uri_slice, features, info_data, region_param)

    def test_upscaling_ok_max_syntax(self):
        uri_slice = "^max"
        features = "sizeUpscaling"
        info_data = self.mock_info(8000, 6001)
        region_param = self.mock_region(399, 299)
        SizeParameter(uri_slice, features, info_data, region_param)

    def test_width_larger_than_max_raises(self):
        uri_slice = "5000,"
        features = ("sizeByW", "sizeUpscaling")
        info_data = self.mock_info(8000, 6001, max_width=4000)
        region_param = self.mock_region(4000, 3000)
        with pytest.raises(RequestException) as re:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "Image would be upsampled" in re.value.message

    def test_height_larger_than_max_raises(self):
        uri_slice = ",1024"
        features = "sizeByH"
        info_data = self.mock_info(8000, 6001, max_height=1000)
        region_param = self.mock_region(2048, 2048)
        with pytest.raises(RequestException) as re:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "height (1024) is greater" in re.value.message

    def test_area_larger_than_max_raises(self):
        uri_slice = "5000,"
        features = ("sizeByW", "sizeUpscaling")
        info_data = self.mock_info(8000, 6001, max_area=16000000)
        region_param = self.mock_region(5000, 6000)
        with pytest.raises(RequestException) as re:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "area (30000000) is greater" in re.value.message

    def test_can_get_tiles_without_sizeByW_if_allowed(self):
        uri_slice = "1024,"
        features = ()
        tiles = [Tile(1024, [1, 2, 4, 8, 16])]
        info_data = self.mock_info(8000, 6000, tiles=tiles)
        region_param = self.mock_region(1024, 1024)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 1024
        assert sp.height == 1024

    def test_can_get_right_edge_tiles_without_sizeByW_if_allowed(self):
        uri_slice = "30,"
        features = ()
        tiles = [Tile(1024, [1, 2, 4, 8, 16])]
        info_data = self.mock_info(2078, 6000, tiles=tiles)
        region_param = self.mock_region(60, 2048)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 30
        assert sp.height == 1024

    def test_can_get_bottom_row_tiles_without_sizeByW_if_allowed(self):
        uri_slice = "1024,"
        features = ()
        tiles = [Tile(1024, [1, 2, 4, 8, 16])]
        info_data = self.mock_info(8000, 6000, tiles=tiles)
        region_param = self.mock_region(4096, 3520)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 1024
        assert sp.height == 880

    def test_normal_sizeByW_raises(self):
        uri_slice = "1025,"  # off by one; could be arbirary
        features = ()
        tiles = [Tile(1024, [1, 2, 4, 8, 16])]
        info_data = self.mock_info(8000, 6000, tiles=tiles)
        region_param = self.mock_region(4096, 3520)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_param)
        assert "not support the 'sizeByW'" in fe.value.message

    def test_can_get_small_sizes_without_sizeByW_if_allowed(self):
        uri_slice = "1000,"
        features = ()
        tiles = [Tile(1024, [1, 2, 4, 8, 16])]
        sizes = [Size(1000, 750), Size(500, 375), Size(250, 187)]
        info_data = self.mock_info(8000, 6000, sizes=sizes, tiles=tiles)
        region_param = self.mock_region(8000, 6000)
        sp = SizeParameter(uri_slice, features, info_data, region_param)
        assert sp.width == 1000
        assert sp.height == 750
