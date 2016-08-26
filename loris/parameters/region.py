from decimal import Decimal
from math import floor

from loris.constants import DECIMAL_ONE
from loris.constants import DECIMAL_ONE_HUNDRED
from loris.constants import FULL
from loris.constants import REGION_BY_PCT
from loris.constants import REGION_BY_PIXEL
from loris.constants import REGION_SQUARE
from loris.constants import SQUARE
from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import RequestException
from loris.exceptions import SyntaxException
from loris.parameters.api import AbstractParameter

class RegionParameter(AbstractParameter):
    # Almost all of the methods here could be static, but passing stuff
    # around was starting to get messy.

    def __init__(self, uri_slice, enabled_features, info_data):
        super().__init__(uri_slice, enabled_features)
        self.info_data = info_data
        self.decimal_x = None
        self.decimal_y = None
        self.decimal_w = None
        self.decimal_h = None
        self.pixel_x = None
        self.pixel_y = None
        self.pixel_w = None
        self.pixel_h = None
        self._request_type = None

        # raises SyntaxException, RequestException
        self._initialize_properites()

        # raises RequestException, FeatureNotEnabledException
        self._run_checks()

    @property
    def request_type(self):
        # raises SyntaxException
        if self._request_type is None:
            self._request_type = self._deduce_request_type()
        return self._request_type

    @property
    def canonical(self):
        if self._canonical is None:
            if self.request_type is not FULL:
                px = (self.pixel_x, self.pixel_y, self.pixel_w, self.pixel_h)
                self._canonical = ','.join(map(str, px))
            else:
                self._canonical = FULL
        return self._canonical

    def _initialize_properites(self):
        # raises SyntaxException
        # raises RequestException
        if self.request_type is FULL:
            self._init_full_request(self.info_data); return
        if self.request_type is REGION_SQUARE:
            self._init_square_request(self.info_data); return
        if self.request_type is REGION_BY_PIXEL:
            xywh = tuple(map(int, self.uri_slice.split(',')))
            self._init_pixel_request(xywh, self.info_data); return
        if self.request_type is REGION_BY_PCT:
            xywh = tuple(map(float, self.uri_slice.split(':')[1].split(',')))
            self._init_pct_request(xywh, self.info_data); return

    def _run_checks(self):
        # raises RequestException
        self._check_for_oob_errors()
        self._adjust_to_in_bounds()
        # raises FeatureNotEnabledException
        self._check_if_supported()
        self._adjust_if_actually_full()

    def _deduce_request_type(self):
        if self.uri_slice is FULL:
            return FULL
        elif self.uri_slice == SQUARE:
            return REGION_SQUARE
        elif all([n.isdigit() for n in self.uri_slice.split(',')]):
            # For REGION_BY_PIXEL and REGION_BY_PCT we'll raise later if there are too many ',' tokens
            return REGION_BY_PIXEL
        elif self.uri_slice.split(':')[0] == 'pct':
            return REGION_BY_PCT
        msg = 'Region syntax "{0}" is not valid.'.format(self.uri_slice)
        raise SyntaxException(msg)

    def _init_full_request(self, info_data):
        self.pixel_x = 0
        self.decimal_x = 0
        self.pixel_y = 0
        self.decimal_y = 0
        self.pixel_w = info_data.width
        self.decimal_w = DECIMAL_ONE
        self.pixel_h = info_data.height
        self.decimal_h = DECIMAL_ONE

    def _init_square_request(self, info_data):
        region = None
        if info_data.width > info_data.height:
            offset = (info_data.width - info_data.height) // 2
            region = (offset, 0, info_data.height, info_data.height)
        else:
            offset = (info_data.height - info_data.width) // 2
            region = (0, offset, info_data.width, info_data.width)
        return self._init_pixel_request(region, info_data)

    def _init_pixel_request(self, xywh, info_data):
        # raises SyntaxException
        try:
            self.pixel_x, self.pixel_y, self.pixel_w, self.pixel_h = xywh
        except ValueError:
            msg = 'Four points are required for pixel regions (request was: {0})'
            raise SyntaxException(msg.format(self.uri_slice))
        self.decimal_x = self.pixel_x / Decimal(info_data.width)
        self.decimal_y = self.pixel_y / Decimal(info_data.height)
        self.decimal_w = self.pixel_w / Decimal(info_data.width)
        self.decimal_h = self.pixel_h / Decimal(info_data.height)

    def _init_pct_request(self, xywh, info_data):
        # raises RequestException
        # raises SyntaxException
        if any(n > DECIMAL_ONE_HUNDRED for n in xywh):
            msg = 'Region percentages must be less than or equal to 100 (request was: {0})'
            raise RequestException(msg.format(self.uri_slice))
        if any((n <= 0) for n in xywh[2:]):
            msg = 'Width and Height percentages must be greater than 0 (request was: {0})'
            raise RequestException(msg.format(self.uri_slice))

        try:
            px_xywh = map(RegionParameter._pct_to_decimal, xywh)
            self.decimal_x, self.decimal_y, self.decimal_w, self.decimal_h = px_xywh
        except ValueError:
            msg = 'Four points are required for pct regions (request was: {0})'
            raise SyntaxException(msg.format(self.uri_slice))

        self.pixel_x = int(floor(self.decimal_x * info_data.width))
        self.pixel_y = int(floor(self.decimal_y * info_data.height))
        self.pixel_w = int(floor(self.decimal_w * info_data.width))
        self.pixel_h = int(floor(self.decimal_h * info_data.height))

    @staticmethod
    def _pct_to_decimal(n):
        return Decimal(n) / DECIMAL_ONE_HUNDRED

    def _adjust_to_in_bounds(self):
        # w and h can be out of bounds
        w_oob = (self.decimal_x + self.decimal_w) > DECIMAL_ONE
        h_oob = (self.decimal_y + self.decimal_h) > DECIMAL_ONE
        if w_oob:
            self.decimal_w = DECIMAL_ONE - self.decimal_x
            self.pixel_w = self.info_data.width - self.pixel_x
        if h_oob:
            self.decimal_h = DECIMAL_ONE - self.decimal_y
            self.pixel_h = self.info_data.height - self.pixel_y
        if all((self.decimal_x == 0, self.decimal_y == 0, w_oob, h_oob)):
            self._canonical = FULL

    def _check_for_oob_errors(self):
        # x and y must be in bounds
        if any(axis < 0 for axis in (self.pixel_x, self.pixel_y)):
            msg = 'x and y region parameters must be 0 or greater '
            msg += '(original_request: {0}).'
            raise RequestException(msg.format(self.uri_value))
        if self.pixel_x >= self.info_data.width:
            msg = 'Region x parameter is greater than the width of the image. '
            msg += 'Image width is {0}.'
            raise RequestException(msg.format(self.info_data.width))
        if self.pixel_y >= self.info_data.height:
            msg = 'Region y parameter is greater than the height of the image. '
            msg += 'Image height is {0}.'
            raise RequestException(msg.format(self.info_data.height))

    def _check_if_supported(self):
        if self.request_type is FULL:
            return
        try:
            if self._request_type not in self.enabled_features:
                raise FeatureNotEnabledException(self._request_type)
        except FeatureNotEnabledException as fe:
            # If app configs allow for a set of tiles / sizes this will be in
            # info_data. We check scale factors in the SizeParameter
            if self._allowed_level0_tile_request():
                return
            else:
                raise

    def _adjust_if_actually_full(self):
        px = '0,0,{0},{1}'.format(self.info_data.width, self.info_data.height)
        if self.uri_slice == px:
            self._request_type = FULL
            self._canonical = FULL

    def _allowed_level0_tile_request(self):
        if self.info_data.tiles:
            tile_width = self.info_data.tiles[0]['width']
            tile_height = self.info_data.tiles[0].get('height', tile_width)
            image_width = self.info_data.width
            image_height = self.info_data.height
            x, y, w, h = map(int, self.canonical.split(','))
            # TODO: We should really be checking scale factors...:
            # (w / tile_width) in scale_factors or w / (image_width % tile_width) in scale_factors
            # (h / tile_height) in scale_factors or h / (image_height % tile_height) in scale_factors
            # ...something like that.
            requirements = (
                x % tile_width == 0,
                y % tile_height == 0,
                (w in (tile_width, image_width % tile_width) or w % tile_width == 0),
                (h in (tile_height, image_height % tile_height) or h % tile_height == 0)
            )
            return all(requirements)
        else:
            return False
