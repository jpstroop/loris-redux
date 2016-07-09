from decimal import Decimal
from loris.exceptions.request_exception import RequestException
from loris.exceptions.syntax_exception import SyntaxException
from loris.exceptions.feature_not_enabled_exception import FeatureNotEnabledException
from loris.parameters.region import RegionParameter
from loris.parameters.region import FULL
from loris.parameters.region import SQUARE
from loris.parameters.region import PCT
from loris.parameters.region import PIXEL
from loris.parameters.region import DECIMAL_ONE
from unittest.mock import Mock
import pytest

class TestRegionParameter(object):

    def test__deduce_request_type_raises_syntax_exception(self):
        info_data = Mock(width=4637, height=7201)
        with pytest.raises(SyntaxException) as se:
            RegionParameter('wtf', (), info_data)
        assert 'Region syntax "wtf" is not valid.' == se.value.message

    def test__check_if_supported_px_raises(self):
        info_data = Mock(width=4637, height=7201, tiles=[{'width':512}])
        features = ('regionByPct', 'regionSquare')
        with pytest.raises(FeatureNotEnabledException) as fe:
            RegionParameter('4,5,6,7', features, info_data)
        assert 'This server does not support requesting regions by pixel' == fe.value.message
        assert fe.value.feature == 'regionByPx'

    def test__check_if_supported_pct_raises(self):
        info_data = Mock(width=4637, height=7201, tiles=[{'width':512}])
        features = ('regionByPx', 'regionSquare')
        with pytest.raises(FeatureNotEnabledException) as fe:
            RegionParameter('pct:8,9,10,11', features, info_data)
        assert 'This server does not support requesting regions by percent' == fe.value.message
        assert fe.value.feature == 'regionByPct'

    def test__check_if_supported_square_raises(self):
        info_data = Mock(width=4637, height=7201, tiles=[{'width':512}])
        features = ('regionByPx', 'regionByPct')
        with pytest.raises(FeatureNotEnabledException) as fe:
            RegionParameter('square', features, info_data)
        assert 'This server does not support the "square" keyword' == fe.value.message
        assert fe.value.feature == 'regionSquare'

    def test__init_full_request(self):
        info_data = Mock(width=4637, height=7201)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        rp = RegionParameter('full', features, info_data)
        assert rp.canonical is FULL
        assert rp.pixel_x == 0
        assert rp.pixel_y == 0
        assert rp.pixel_w == info_data.width
        assert rp.pixel_h == info_data.height
        assert rp.decimal_x == 0
        assert rp.decimal_y == 0
        assert rp.decimal_w == DECIMAL_ONE
        assert rp.decimal_h == DECIMAL_ONE

    def test__init_square_request_portrait(self):
        info_data = Mock(width=4638, height=7201)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        rp = RegionParameter('square', features, info_data)
        assert rp.request_type is SQUARE
        assert rp.canonical == '0,1281,4638,4638'
        assert rp.pixel_x == 0
        assert rp.pixel_y == 1281
        assert rp.pixel_w == 4638
        assert rp.pixel_h == 4638
        assert rp.decimal_x == 0
        assert rp.decimal_y == Decimal('0.1778919594500763782807943341')
        assert rp.decimal_w == 1
        assert rp.decimal_h == Decimal('0.6440772114984029995833911957')

    def test__init_square_request_landscape(self):
        info_data = Mock(width=8400, height=3000)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        rp = RegionParameter('square', features, info_data)
        assert rp.canonical == '2700,0,3000,3000'
        assert rp.request_type is SQUARE
        assert rp.pixel_x == 2700
        assert rp.pixel_y == 0
        assert rp.pixel_w == 3000
        assert rp.pixel_h == 3000
        assert rp.decimal_x == Decimal('0.3214285714285714285714285714')
        assert rp.decimal_y == 0
        assert rp.decimal_w == Decimal('0.3571428571428571428571428571')
        assert rp.decimal_h == 1

    def test__init_pct_request(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        rp = RegionParameter('pct:20,40,15,30', features, info_data)
        assert rp.canonical == '691,2880,518,2160'
        assert rp.request_type is PCT
        assert rp.pixel_x == 691
        assert rp.pixel_y == 2880
        assert rp.pixel_w == 518
        assert rp.pixel_h == 2160
        assert rp.decimal_x == Decimal('0.2')
        assert rp.decimal_y == Decimal('0.4')
        assert rp.decimal_w == Decimal('0.15')
        assert rp.decimal_h == Decimal('0.3')

    def test__init_pct_request_raises_request_exception_gt_100(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        with pytest.raises(RequestException) as re:
            RegionParameter('pct:101,40,20,20', features, info_data)
        assert 'less than or equal to 100' in re.value.message

    def test__init_pct_request_raises_request_exception_lt_0(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        with pytest.raises(RequestException) as re:
            RegionParameter('pct:50,40,0,20', features, info_data)
        assert 'must be greater than 0' in re.value.message

    def test__init_pct_request_raises_syntax_exception(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        with pytest.raises(SyntaxException) as se:
            RegionParameter('pct:50,40,2', features, info_data)
        assert 'Four points are required' in se.value.message

    def test__init_pixel_request(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        rp = RegionParameter('600,1357,1567,2590', features, info_data)
        assert rp.canonical == '600,1357,1567,2590'
        assert rp.request_type is PIXEL
        assert rp.pixel_x == 600
        assert rp.pixel_y == 1357
        assert rp.pixel_w == 1567
        assert rp.pixel_h == 2590
        assert rp.decimal_x == Decimal('0.1736111111111111111111111111')
        assert rp.decimal_y == Decimal('0.1884722222222222222222222222')
        assert rp.decimal_w == Decimal('0.4534143518518518518518518519')
        assert rp.decimal_h == Decimal('0.3597222222222222222222222222')

    def test__init_pixel_request_raises_syntax_exception(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        with pytest.raises(SyntaxException) as se:
            RegionParameter('600,1357,1567', features, info_data)
        assert 'Four points are required' in se.value.message

    def test_requests_wide_adjusts_to_in_bounds(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        rp = RegionParameter('0,0,500,7201', features, info_data)
        assert rp.canonical == '0,0,500,7200'

    def test_requests_tall_adjusts_to_in_bounds(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        rp = RegionParameter('0,0,3457,200', features, info_data)
        assert rp.canonical == '0,0,3456,200'

    def test_requests_adjusts_canonical_to_full_if_appropriate(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        rp = RegionParameter('0,0,3457,7201', features, info_data)
        assert rp.canonical == FULL
        assert rp.pixel_x == 0
        assert rp.decimal_x == 0
        assert rp.pixel_y == 0
        assert rp.decimal_y == 0
        assert rp.pixel_w == info_data.width
        assert rp.decimal_w == DECIMAL_ONE
        assert rp.pixel_h == info_data.height
        assert rp.decimal_h == DECIMAL_ONE

    def test_oob_x_raises_request_exception(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        with pytest.raises(RequestException) as re:
            RegionParameter('3457,1234,1234,1234', features, info_data)
        assert 'Region x parameter is greater than the width' in re.value.message

    def test_oob_y_raises_request_exception(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        with pytest.raises(RequestException) as re:
            RegionParameter('0,7201,1234,1234', features, info_data)
        assert 'Region y parameter is greater than the height' in re.value.message

    def test_strange_syntax_raises_1(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        with pytest.raises(SyntaxException) as se:
            RegionParameter('4,8,15,16,23,42', features, info_data)
        assert 'Four points' in se.value.message

    def test_strange_syntax_raises_2(self):
        info_data = Mock(width=3456, height=7200)
        features = ('regionByPct', 'regionSquare', 'regionByPx')
        with pytest.raises(SyntaxException) as se:
            RegionParameter('foobar', features, info_data)
        assert 'Region syntax "foobar"' in se.value.message

    def test_can_get_without_rPx_tiles_if_allowed(self):
        info_data = Mock(width=3456, height=7200, tiles=[{'width':1024}])
        features = () # regionByPx disabled
        # None of these should raise:
        RegionParameter('0,0,1024,1024', features, info_data)
        RegionParameter('1024,1024,1024,1024', features, info_data)
        RegionParameter('0,0,2048,2048', features, info_data)
        # Bottom row
        RegionParameter('0,7168,1024,32', features, info_data)
        # Right column
        RegionParameter('3072,0,384,1024', features, info_data)
        # Bottom right corner
        RegionParameter('3072,7168,384,32', features, info_data)
        # Bottom right corner, adjusts to in bounds
        RegionParameter('3072,7168,385,33', features, info_data)

    def test_get_rPx_tiles_raises_if_wrong_region_x(self):
        info_data = Mock(width=3456, height=7200, tiles=[{'width':1024}])
        features = () # regionByPx disabled
        with pytest.raises(FeatureNotEnabledException) as fe:
            RegionParameter('1023,0,1024,1024', features, info_data)

    def test_get_rPx_tiles_raises_if_wrong_region_y(self):
        info_data = Mock(width=3456, height=7200, tiles=[{'width':1024}])
        features = () # regionByPx disabled
        with pytest.raises(FeatureNotEnabledException) as fe:
            RegionParameter('2048,2047,1024,1024', features, info_data)

    def test_get_rPx_tiles_raises_if_wrong_region_w(self):
        info_data = Mock(width=3456, height=7200, tiles=[{'width':1024}])
        features = () # regionByPx disabled
        with pytest.raises(FeatureNotEnabledException) as fe:
            RegionParameter('0,0,1023,1024', features, info_data)

    def test_get_rPx_tiles_raises_if_wrong_region_h(self):
        info_data = Mock(width=3456, height=7200, tiles=[{'width':1024}])
        features = () # regionByPx disabled
        with pytest.raises(FeatureNotEnabledException) as fe:
            RegionParameter('1024,2048,2048,1025', features, info_data)
