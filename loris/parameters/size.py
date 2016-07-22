from decimal import Decimal
from loris.exceptions.request_exception import RequestException
from loris.exceptions.syntax_exception import SyntaxException
from loris.exceptions.feature_not_enabled_exception import FeatureNotEnabledException
from loris.parameters.api import AbstractParameter
from math import floor
import re

# Maximum approximation error between the original dimensions and smaller
# requests before we consider a w,h request THAT IS NOT THE SIZES LIST
# to be 'sizeByDistortedWh', e.g.:
#
# >>> MAX_WH_ERROR = 0.1
# >>> (3000/2000) - (6000 / 4001)
# 0.0003749062734317299
# >>> (3000/2000) - (6000 / 4001) < MAX_WH_ERROR
# True
#
# This is tricky for two reasons:
# 1) OSd will make requests all the way down to 3:2, 2:1, etc.
# and even if you configure it to not go that low, the relative error can
# get pretty high.
#
# 2) Scrolls:
#
# >>> (152500 / 4000) - (1192 / 32)
# 0.875
#
# TODO: is this really the best approach? Seems like we should be able to know
# that the error is going to be larger when the aspect ratio is greater?
MAX_WH_ERROR = 0.01

FULL = 'full'
MAX = 'max'
BY_W = 'sizeByW'
BY_H = 'sizeByH'
BY_PCT = 'sizeByPct'
BY_CONFINED_WH = 'sizeByConfinedWh'
BY_DISTORTED_WH = 'sizeByDistortedWh'
BY_WH = 'sizeByWh'

DECIMAL_ONE_HUNDRED = Decimal(100.0)

W_REGEX = re.compile(r'^\d+,$')
H_REGEX = re.compile(r'^,\d+$')
WH_REGEX = re.compile(r'^\d+,\d+$')
CONFINED_REGEX = re.compile(r'^!\d+,\d+$')

class SizeParameter(AbstractParameter):

    def __init__(self, uri_slice, enabled_features, info_data, region_w, region_h):
        super().__init__(uri_slice, enabled_features, info_data)
        self.region_w = region_w
        self.region_h = region_h
        self.width = None
        self.height = None
        self.max_width = self.info_data.profile[1].get('maxWidth', region_w)
        self.max_height = self.info_data.profile[1].get('maxHeight', region_h)
        self.max_area = self.info_data.profile[1].get('maxArea', region_w * region_h)
        self._canonical = None
        self._request_type = None
        self._distort_aspect = False

        # raises SyntaxException, RequestException
        self._initialize_properites()

        # raises RequestException
        # self._check_size_above_full()

        # raises FeatureNotEnabledException
        # Note that this has to happen after we know the w/h in case this is
        # a level 0 config with tile support enabled.

        self._check_if_supported()
        # Re ^^ check features (can probably do in a loop) and also we don't
        # adjust for max* so need to check and raise RequestException

        self._adjust_if_actually_full() # TODO what about MAX? Same? Spec doesn't say??

    @property
    def request_type(self):
        # raises SyntaxException
        # raises FeatureNotEnabledException
        if self._request_type is None:
            self._request_type = self._deduce_request_type()
            self._check_if_supported()
        return self._request_type

    @property
    def canonical(self):
        if self._canonical is None:
            # TODO
            pass
        return self._canonical

    def _deduce_request_type(self):
        if self.uri_slice == FULL:
            return FULL
        if self.uri_slice == MAX:
            return MAX
        if re.match(W_REGEX, self.uri_slice):
            return BY_W
        if re.match(H_REGEX, self.uri_slice):
            return BY_H
        if re.match(WH_REGEX, self.uri_slice):
            if SizeParameter._is_distorted(self.uri_slice, self.info_data):
                return BY_DISTORTED_WH
            else:
                return BY_WH
        if re.match(CONFINED_REGEX, self.uri_slice):
            return BY_CONFINED_WH
        if self.uri_slice.split(':')[0] == 'pct':
            return BY_PCT
        msg = 'Size syntax "{0}" is not valid.'.format(self.uri_slice)
        raise SyntaxException(msg)

    @staticmethod
    def _is_distorted(uri_slice, info_data):
        # static and passing vals so that we can test this method in isolation
        w, h = map(int, uri_slice.split(','))
        try:
            if { 'width' : w, 'height' : h } in info_data.sizes:
                return False
        except TypeError:
             # raised w/ unhashable type: 'dict' if we have exactly one size
             pass
        else:
            aspect = info_data.long_dim / info_data.short_dim
            request_aspect = max(w, h) / min(w, h)
            # we have to account for sizeAboveFull
            larger_aspect = max(aspect, request_aspect)
            smaller_aspect = min(aspect, request_aspect)
            return larger_aspect - smaller_aspect > MAX_WH_ERROR

    def _adjust_if_actually_full(self):
        if self.region_w == self.width and self.region_h == self.height:
            self._request_type = FULL
            self._canonical = FULL

    def _initialize_properites(self):
        # raises SyntaxException, RequestException
        if self.request_type is FULL:
            self._init_full_request(); return
        if self.request_type is MAX:
            self._init_max_request(); return
        if self.request_type is BY_W:
            self._init_by_w_request(); return
        if self.request_type is BY_H:
            self._init_by_h_request(); return
        if self.request_type is BY_PCT:
            self._init_by_pct_request(); return
        if self.request_type is BY_CONFINED_WH:
            self._init_by_confined_wh_request(); return
        if self.request_type is BY_WH:
            self._init_wh_request(distort_aspect=False); return
        if self.request_type is BY_DISTORTED_WH:
            self._init_wh_request(distort_aspect=True); return

    def _init_full_request(self):
        self.width = self.region_w
        self.height = self.region_h

    def _init_max_request(self):
        self.width = self.region_w
        self.height = self.region_h
        if (self.width * self.height) > self.max_area:
            # TODO: seems like this could be more precise. Test is often
            # 1px short (on the long dim?)
            scale = (self.max_area / (self.width * self.height))**0.5
            self.width = floor(self.region_w * scale)
            self.height = floor(self.region_h * scale)
        if self.width > self.max_width:
            scale = self.max_width / self.region_w
            self.width = floor(self.region_w * scale)
            self.height = floor(self.region_h * scale)
        if self.height > self.max_height:
            scale = self.max_height / self.region_h
            self.width = floor(self.region_w * scale)
            self.height = floor(self.region_h * scale)

    def _init_by_w_request(self):
        self.width = int(self.uri_slice[:-1])
        scale = self.width / self.region_w
        self.height = floor(self.region_h * scale)

    def _init_by_h_request(self):
        self.height = int(self.uri_slice[1:])
        scale = self.height / self.region_h
        self.width = floor(self.region_w * scale)

    def _init_by_pct_request(self):
        scale = SizeParameter._pct_to_decimal(self.uri_slice.split(':')[1])
        if scale <= 0:
            msg = 'Size percentage must be greater than 0 ({0}).'
            raise RequestException(msg.format(self.uri_slice))
        w_decimal = self.region_w * scale
        h_decimal = self.region_h * scale
        # handle teeny, tiny requests.
        self.width = 1 if 0 < w_decimal < 1 else int(w_decimal)
        self.height = 1 if 0 < h_decimal < 1 else int(h_decimal)

    def _init_by_confined_wh_request(self):
        request_w, request_h = map(int, self.uri_slice[1:].split(','))
        # TODO: below may need more precision than we get from floats w/
        # large images.
        scale = min(request_w / self.region_w, request_h / self.region_h)
        self.width = int(self.region_w * scale)
        self.height = int(self.region_h * scale)

    def _init_wh_request(self, distort_aspect=False):
        self._distort_aspect = distort_aspect
        self.width, self.height = map(int, self.uri_slice.split(','))

    @staticmethod
    def _pct_to_decimal(n):
        return Decimal(float(n)) / DECIMAL_ONE_HUNDRED

    def _check_if_supported(self):
        # raises FeatureNotEnabledException
        try:
            if self._request_type not in self.enabled_features:
                raise FeatureNotEnabledException(self._request_type)
        except FeatureNotEnabledException as fe:
            if self._allowed_level0_size_request():
                pass
            else:
                raise

    def _allowed_level0_size_request(self):
        if self.info_data.sizes: # calc the scales, see if the size is one of them
            pass
        else:
            return False
