from loris.constants import FULL
from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import RequestException
from loris.exceptions import SyntaxException
from loris.parameters.size import SizeParameter

from unittest.mock import Mock

import pytest

class TestSizeParameter(object):

    def mock_info(self, width, height, **kwargs):
        long_dim = max(width, height)
        short_dim = min(width, height)
        sizes = kwargs.get('sizes', [{ 'width': width, 'height': height }])
        tiles = kwargs.get('tiles', None)
        profile = kwargs.get('profile', ['',{}])
        return Mock(width=width, height=height, long_dim=long_dim, \
            short_dim=short_dim, sizes=sizes, tiles=tiles, profile=profile)

    def test__is_distorted_no_sizes_within_error(self):
        uri_slice = '4000,3000'
        info_data = self.mock_info(8000, 6001)
        assert SizeParameter._is_distorted(uri_slice, info_data) is False

    def test__is_distorted_no_sizes_outside_error(self):
        uri_slice = '4000,2975'
        info_data = self.mock_info(8000, 6001)
        assert SizeParameter._is_distorted(uri_slice, info_data)

    def test__is_distorted_overridden_by_sizes(self):
        uri_slice = '1192,32'
        sizes = [
            { 'width': 1192, 'height': 32 },
            { 'width': 2383, 'height': 63 },
            # ...
            { 'width': 76250, 'height': 2000 },
        ]
        info_data = self.mock_info(152500, 4000, sizes=sizes)
        assert SizeParameter._is_distorted(uri_slice, info_data) is False

    def test__deduce_request_type_raises_syntax_exception(self):
        uri_slice = 'wtf'
        info_data = self.mock_info(8000, 6001)
        features = ()
        region_w, region_h = (400, 300)
        with pytest.raises(SyntaxException) as se:
            _ = SizeParameter(uri_slice, features, info_data, region_w, region_h).request_type
        assert 'Size syntax "wtf" is not valid.' == se.value.message

    def test__init_full(self):
        uri_slice = 'full'
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (3456, 1234)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 3456
        assert sp.height == 1234
        assert sp.canonical is FULL

    def test__init_max_size_ok(self):
        uri_slice = 'max'
        features = ('max')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (3456, 1234)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 3456
        assert sp.height == 1234
        assert sp.canonical is FULL # gets adjusted

    def test__init_max_over_size_w(self):
        uri_slice = 'max'
        features = ('max')
        profile = ['', { 'maxWidth' : 4000}]
        info_data = self.mock_info(8000, 6001, profile=profile)
        region_w, region_h = (5000, 2000) # 1000 wider than allowed
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 4000
        assert sp.height == 1600
        assert sp.canonical == '4000,'

    def test__init_max_over_size_h(self):
        uri_slice = 'max'
        features = ('max')
        profile = ['', { 'maxHeight' : 4000}]
        info_data = self.mock_info(8000, 6000, profile=profile)
        region_w, region_h = (5000, 4500) # 500 higher than allowed
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 4444
        assert sp.height == 4000
        assert sp.canonical == '4444,'

    def test__init_max_over_size_area(self):
        uri_slice = 'max'
        features = ('max')
        max_area = 24000000
        profile = ['', { 'maxArea' : 24000000}]
        info_data = self.mock_info(8000, 6000, profile=profile)
        region_w, region_h = (5000, 7000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 4140
        assert sp.height == 5796
        assert (sp.height*sp.width) < max_area
        assert sp.canonical == '4140,'

    def test__check_if_supported_max_raises(self):
        uri_slice = 'max'
        features = ()
        max_area = 24000000
        profile = ['', { 'maxArea' : 24000000}]
        info_data = self.mock_info(8000, 6000, profile=profile)
        region_w, region_h = (5000, 7000)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'max'" in fe.value.message

    def test__init_sizeByW(self):
        uri_slice = '1024,'
        features = ('sizeByW')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2048, 2048)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1024
        assert sp.height == 1024
        assert sp.canonical == '1024,'

    def test__check_if_supported_sizeByW_raises(self):
        uri_slice = '1024,'
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2048, 2048)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByW'" in fe.value.message

    def test_full_as_sizeByW_adjusts_request_type(self):
        uri_slice = '1024,'
        features = ('sizeByW')
        info_data = self.mock_info(8000, 6000)
        region_w, region_h = (1024, 1024)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1024
        assert sp.height == 1024
        assert sp.request_type is FULL
        assert sp.canonical == FULL

    def test_full_as_sizeByW_still_raises(self):
        uri_slice = '1024,'
        features = ()
        info_data = self.mock_info(8000, 6000)
        region_w, region_h = (1024, 1024)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByW'" in fe.value.message

    def test__init_sizeByH(self):
        uri_slice = ',1024'
        features = ('sizeByH')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2048, 3072)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 682
        assert sp.height == 1024
        assert sp.canonical == '682,'

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByH_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByH_still_raises(self):
        raise NotImplementedError

    def test__check_if_supported_sizeByH_raises(self):
        uri_slice = ',1024'
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2048, 3072)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByH'" in fe.value.message

    def test__init_sizeByPct(self):
        uri_slice = 'pct:20'
        features = ('sizeByPct')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 400
        assert sp.height == 600
        assert sp.canonical == '400,'

    def test__check_if_supported_sizeByPct_raises(self):
        uri_slice = 'pct:20'
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByPct'" in fe.value.message

    def test_pct_request_round_lt_0_to_1(self):
        uri_slice = 'pct:0.01'
        features = ('sizeByPct')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1
        assert sp.height == 1
        assert sp.canonical == '1,'

    def test_pct_0_raises(self):
        uri_slice = 'pct:0'
        features = ('sizeByPct')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        with pytest.raises(RequestException) as se:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert 'Size percentage must be greater than 0 (pct:0).' == se.value.message

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByPct_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByPct_still_raises(self):
        raise NotImplementedError

    def test__init_sizeByConfinedWh_portrait(self):
        uri_slice = '!200,200'
        features = ('sizeByConfinedWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 133
        assert sp.height == 200
        assert sp.canonical == '133,'

    def test__init_sizeByConfinedWh_landscape(self):
        uri_slice = '!300,300'
        features = ('sizeByConfinedWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 1200)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 300
        assert sp.height == 180
        assert sp.canonical == '300,'

    def test__check_if_supported_sizeByConfinedWh_raises(self):
        uri_slice = '!200,200'
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByConfinedWh'" in fe.value.message

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByConfinedWh_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByConfinedWh_still_raises(self):
        raise NotImplementedError

    def test__init_sizeByDistortedWh(self):
        uri_slice = '500,600'
        features = ('sizeByDistortedWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 1200)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 500
        assert sp.height == 600
        assert sp._distort_aspect
        assert sp.canonical == '500,600'

    def test__check_if_supported_sizeByDistortedWh_raises(self):
        uri_slice = '2,2000'
        features = ('sizeAboveFull')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 1200)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByDistortedWh'" in fe.value.message

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByDistortedWh_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByDistortedWh_still_raises(self):
        raise NotImplementedError

    def test__init_sizeByWh(self):
        uri_slice = '400,300'
        features = ('sizeByWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (8000, 6001)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 400
        assert sp.height == 300
        assert not sp._distort_aspect
        assert sp.canonical == '400,'

    def test__check_if_supported_sizeByWh_raises(self):
        uri_slice = '400,300'
        features = ()
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (8000, 6001)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByWh'" in fe.value.message

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByWh_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByWh_still_raises(self):
        raise NotImplementedError

    def test__sizeAboveFull_ok(self):
        uri_slice = '400,300'
        features = ('sizeByWh', 'sizeAboveFull')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (399, 299)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 400
        assert sp.height == 300
        assert sp.canonical == '400,'

    def test_sizeAboveFull_raises(self):
        uri_slice = '400,300'
        features = ('sizeByWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (399, 299)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeAboveFull'" in fe.value.message

    def test_width_larger_than_max_raises(self):
        uri_slice = '5000,'
        features = ('sizeByW', 'sizeAboveFull')
        profile = ['', { 'maxWidth' : 4000 }]
        info_data = self.mock_info(8000, 6001, profile=profile)
        region_w, region_h = (4000, 3000)
        with pytest.raises(RequestException) as re:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "width (5000) is greater" in re.value.message

    def test_height_larger_than_max_raises(self):
        uri_slice = ',1024'
        features = ('sizeByH')
        profile = ['', { 'maxHeight' : 1000 }]
        info_data = self.mock_info(8000, 6001, profile=profile)
        region_w, region_h = (2048, 2048)
        with pytest.raises(RequestException) as re:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "height (1024) is greater" in re.value.message

    def test_area_larger_than_max_raises(self):
        uri_slice = '5000,'
        features = ('sizeByW', 'sizeAboveFull')
        profile = ['', { 'maxArea' : 16000000 }]
        info_data = self.mock_info(8000, 6001, profile=profile)
        region_w, region_h = (5000, 6000)
        with pytest.raises(RequestException) as re:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "area (30000000) is greater" in re.value.message

    def test_full_larger_that_max_raises(self):
        uri_slice = 'full'
        features = ()
        profile = ['', { 'maxArea' : 16000000 }]
        info_data = self.mock_info(8000, 6000, profile=profile)
        region_w, region_h = (8000, 6000)
        with pytest.raises(RequestException) as re:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "area (48000000) is greater" in re.value.message



    def test_can_get_tiles_without_sizeByW_if_allowed(self):
        uri_slice = '1024,'
        features = ()
        tiles = [ { 'width' : 1024, 'scaleFactors' : [1, 2, 4, 8, 16] } ]
        info_data = self.mock_info(8000, 6000, tiles=tiles)
        region_w, region_h = (1024, 1024)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1024
        assert sp.height == 1024

    def test_can_get_right_edge_tiles_without_sizeByW_if_allowed(self):
        uri_slice = '30,'
        features = ()
        tiles = [ { 'width' : 1024, 'scaleFactors' : [1, 2, 4, 8, 16] } ]
        info_data = self.mock_info(2078, 6000, tiles=tiles)
        region_w, region_h = (60, 2048)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 30
        assert sp.height == 1024

    def test_can_get_bottom_row_tiles_without_sizeByW_if_allowed(self):
        uri_slice = '1024,'
        features = ()
        tiles = [ { 'width' : 1024, 'scaleFactors' : [1, 2, 4, 8, 16] } ]
        info_data = self.mock_info(8000, 6000, tiles=tiles)
        region_w, region_h = (4096, 3520)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1024
        assert sp.height == 880

    def test_normal_sizeByW_raises(self):
        uri_slice = '1025,' # off by one; could be arbirary
        features = ()
        tiles = [ { 'width' : 1024, 'scaleFactors' : [1, 2, 4, 8, 16] } ]
        info_data = self.mock_info(8000, 6000, tiles=tiles)
        region_w, region_h = (4096, 3520)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByW'" in fe.value.message

    def test_can_get_small_sizes_without_sizeByW_if_allowed(self):
        uri_slice = '1000,'
        features = ()
        tiles = [ { 'width' : 1024, 'scaleFactors' : [1, 2, 4, 8, 16] } ]
        sizes = [
            { 'width' : 1000, 'height' : 750 },
            { 'width' : 500, 'height' : 375 },
            { 'width' : 250, 'height' : 187 }
        ]
        info_data = self.mock_info(8000, 6000, sizes=sizes, tiles=tiles)
        region_w, region_h = (8000, 6000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1000
        assert sp.height == 750
