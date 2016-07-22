from decimal import Decimal
from loris.exceptions.request_exception import RequestException
from loris.exceptions.syntax_exception import SyntaxException
from loris.exceptions.feature_not_enabled_exception import FeatureNotEnabledException
from loris.parameters.size import SizeParameter
from loris.parameters.size import FULL
from loris.parameters.size import BY_PCT
from unittest.mock import Mock
import pytest

class TestSizeParameter(object):

    def mock_info(self, width, height, **kwargs):
        long_dim = max(width, height)
        short_dim = min(width, height)
        sizes = kwargs.get('sizes', [{ 'width': width, 'height': height }])
        profile = kwargs.get('profile', ['',{}])
        return Mock(width=width, height=height, long_dim=long_dim, \
            short_dim=short_dim, sizes=sizes, profile=profile)

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
        features = ('full', 'full')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (3456, 1234)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 3456
        assert sp.height == 1234

    def test__init_max_size_ok(self):
        uri_slice = 'max'
        features = ('full', 'max')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (3456, 1234)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 3456
        assert sp.height == 1234

    def test__init_max_over_size_w(self):
        uri_slice = 'max'
        features = ('full', 'max')
        profile = ['', { 'maxWidth' : 4000}]
        info_data = self.mock_info(8000, 6001, profile=profile)
        region_w, region_h = (5000, 2000) # 1000 wider than allowed
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 4000
        assert sp.height == 1600

    def test__init_max_over_size_h(self):
        uri_slice = 'max'
        features = ('full', 'max')
        profile = ['', { 'maxHeight' : 4000}]
        info_data = self.mock_info(8000, 6000, profile=profile)
        region_w, region_h = (5000, 4500) # 500 higher than allowed
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 4444
        assert sp.height == 4000

    def test__init_max_over_size_area(self):
        uri_slice = 'max'
        features = ('full', 'max')
        max_area = 24000000
        profile = ['', { 'maxArea' : 24000000}]
        info_data = self.mock_info(8000, 6000, profile=profile)
        region_w, region_h = (5000, 7000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 4140
        assert sp.height == 5796
        assert (sp.height*sp.width) < max_area

    def test__check_if_supported_max_raises(self):
        uri_slice = 'max'
        features = ('full')
        max_area = 24000000
        profile = ['', { 'maxArea' : 24000000}]
        info_data = self.mock_info(8000, 6000, profile=profile)
        region_w, region_h = (5000, 7000)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'max'" in fe.value.message

    def test__init_sizeByW(self):
        uri_slice = '1024,'
        features = ('full', 'sizeByW')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2048, 2048)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1024
        assert sp.height == 1024


    def test__check_if_supported_sizeByW_raises(self):
        uri_slice = '1024,'
        features = ('full')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2048, 2048)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByW'" in fe.value.message

    def test_full_as_sizeByW_adjusts_request_type(self):
        uri_slice = '1024,'
        features = ('full', 'sizeByW')
        info_data = self.mock_info(8000, 6000)
        region_w, region_h = (1024, 1024)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1024
        assert sp.height == 1024
        assert sp.request_type is FULL

    def test_full_as_sizeByW_still_raises(self):
        uri_slice = '1024,'
        features = ('full')
        info_data = self.mock_info(8000, 6000)
        region_w, region_h = (1024, 1024)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByW'" in fe.value.message

    def test__init_sizeByH(self):
        uri_slice = ',1024'
        features = ('full', 'sizeByH')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2048, 3072)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 682
        assert sp.height == 1024

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByH_adjusts_request_type(self):
        raise NotImplementedError

    @pytest.mark.skip(reason='test not written')
    def test_full_as_sizeByH_still_raises(self):
        raise NotImplementedError

    def test__check_if_supported_sizeByH_raises(self):
        uri_slice = ',1024'
        features = ('full')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2048, 3072)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByH'" in fe.value.message

    def test__init_sizeByPct(self):
        uri_slice = 'pct:20'
        features = ('full', 'sizeByPct')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 400
        assert sp.height == 600

    def test__check_if_supported_sizeByPct_raises(self):
        uri_slice = 'pct:20'
        features = ('full')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        with pytest.raises(FeatureNotEnabledException) as fe:
            SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert "not support the 'sizeByPct'" in fe.value.message

    def test_pct_request_round_lt_0_to_1(self):
        uri_slice = 'pct:0.01'
        features = ('full', 'sizeByPct')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 1
        assert sp.height == 1

    def test_pct_0_raises(self):
        uri_slice = 'pct:0'
        features = ('full', 'sizeByPct')
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
        features = ('full', 'sizeByConfinedWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 3000)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 133
        assert sp.height == 200

    def test__init_sizeByConfinedWh_landscape(self):
        uri_slice = '!300,300'
        features = ('full', 'sizeByConfinedWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 1200)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 300
        assert sp.height == 180

    def test__check_if_supported_sizeByConfinedWh_raises(self):
        uri_slice = '!200,200'
        features = ('full')
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
        uri_slice = '2,2000'
        features = ('full', 'sizeByDistortedWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (2000, 1200)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 2
        assert sp.height == 2000
        assert sp._distort_aspect

    def test__check_if_supported_sizeByDistortedWh_raises(self):
        uri_slice = '2,2000'
        features = ('full')
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
        features = ('full', 'sizeByWh')
        info_data = self.mock_info(8000, 6001)
        region_w, region_h = (8000, 6001)
        sp = SizeParameter(uri_slice, features, info_data, region_w, region_h)
        assert sp.width == 400
        assert sp.height == 300
        assert not sp._distort_aspect

    def test__check_if_supported_sizeByWh_raises(self):
        uri_slice = '400,300'
        features = ('full')
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

    # def test__check_if_supported_sizeAboveFull_raises(self):
    #     pass

    # def test_canonical(self):
    #     pass
