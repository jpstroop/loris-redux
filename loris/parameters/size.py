from decimal import Decimal
from loris.constants import DECIMAL_ONE_HUNDRED
from loris.constants import FEATURE_SIZE_BY_CONFINED_WH
from loris.constants import FEATURE_SIZE_BY_H
from loris.constants import FEATURE_SIZE_BY_PCT
from loris.constants import FEATURE_SIZE_BY_W
from loris.constants import FEATURE_SIZE_BY_WH
from loris.constants import FEATURE_SIZE_UPSCALING
from loris.constants import KEYWORD_MAX
from loris.constants import KEYWORD_MAX_AREA
from loris.constants import KEYWORD_MAX_HEIGHT
from loris.constants import KEYWORD_MAX_WIDTH
from loris.exceptions import FeatureNotEnabledException
from loris.exceptions import RequestException
from loris.exceptions import SyntaxException
from loris.info.structs.size import Size
from loris.parameters.api import AbstractParameter
from math import floor
from re import compile
from re import match

# Note that these regexes do not account for a leading '^'; we just check for
# that in self._deduce_request_type()
W_REGEX = compile(r"^\d+,$")
H_REGEX = compile(r"^,\d+$")
WH_REGEX = compile(r"^\d+,\d+$")
CONFINED_REGEX = compile(r"^!\d+,\d+$")


class SizeParameter(AbstractParameter):
    def __init__(self, uri_slice, enabled_features, info, region_param):
        super().__init__(uri_slice, enabled_features)
        self.info = info
        # delegations:
        self.region_w = region_param.pixel_w
        self.region_h = region_param.pixel_h
        # calculations:
        self.image_max_width, self.image_max_height = self._calc_image_max_wh()
        self.width = None
        self.height = None
        self.upscaling_requested = False
        # memoized properties:
        self._request_type = None
        # raises SyntaxException, RequestException
        self._initialize_properties()
        # raises FeatureNotEnabledException, RequestException
        self._run_checks()

    @property
    def request_type(self):
        # raises SyntaxException
        # raises FeatureNotEnabledException
        if self._request_type is None:
            self._request_type = self._deduce_request_type()
        return self._request_type

    @property
    def canonical(self):
        if self._canonical is None:
            if self.request_type is KEYWORD_MAX:
                self._canonical = KEYWORD_MAX
            else:
                self._canonical = f"{self.width},{self.height}"
        return self._canonical

    def _initialize_properties(self):
        # raises SyntaxException, RequestException
        if self.request_type is KEYWORD_MAX:
            self._init_max_request()
            return
        if self.request_type is FEATURE_SIZE_BY_W:
            self._init_by_w_request()
            return
        if self.request_type is FEATURE_SIZE_BY_H:
            self._init_by_h_request()
            return
        if self.request_type is FEATURE_SIZE_BY_PCT:
            self._init_by_pct_request()
            return
        if self.request_type is FEATURE_SIZE_BY_CONFINED_WH:
            self._init_by_confined_wh_request()
            return
        if self.request_type is FEATURE_SIZE_BY_WH:
            self._init_wh_request()
            return

    def _run_checks(self):
        # raises RequestException
        self._check_size_upscaling()
        # raises FeatureNotEnabledException
        self._check_if_supported()
        # raises RequestException
        self._check_if_larger_than_max()
        self._adjust_if_actually_max()

    def _deduce_request_type(self):
        slice = self.uri_slice
        if slice[0:1] == "^":
            self.upscaling_requested = True
            slice = slice[1:]
        if slice == KEYWORD_MAX:
            return KEYWORD_MAX
        if match(W_REGEX, slice):
            return FEATURE_SIZE_BY_W
        if match(H_REGEX, slice):
            return FEATURE_SIZE_BY_H
        if match(WH_REGEX, slice):
            return FEATURE_SIZE_BY_WH
        if match(CONFINED_REGEX, slice):
            return FEATURE_SIZE_BY_CONFINED_WH
        if slice.split(":")[0] == "pct":
            return FEATURE_SIZE_BY_PCT
        msg = f'Size syntax "{self.uri_slice}" is not valid.'
        raise SyntaxException(msg)

    def _adjust_if_actually_max(self):
        if self.image_max_width == self.width and self.image_max_height == self.height:
            self._request_type = KEYWORD_MAX
        if self.region_w == self.width and self.region_h == self.height:
            self._request_type = KEYWORD_MAX

    def _calc_image_max_wh(self):
        # remember, region may be the whole image. it doesn't really matter
        max_w = self.region_w
        max_h = self.region_h
        if self.info.max_area:
            scale = (self.info.max_area / (max_w * max_h)) ** 0.5
            max_w = floor(self.region_w * scale)
            max_h = floor(self.region_h * scale)
        if self.info.max_width and max_w > self.info.max_width:
            scale = self.info.max_width / self.region_w
            max_w = floor(self.region_w * scale)
            max_h = floor(self.region_h * scale)
        if self.info.max_height:
            scale = self.info.max_height / self.region_h
            max_w = floor(self.region_w * scale)
            max_h = floor(self.region_h * scale)
        return (max_w, max_h)

    def _init_max_request(self):
        if self.region_w < self.image_max_width:
            self.width = self.region_w
        else:
            self.width = self.image_max_width
        if self.region_h < self.image_max_height:
            self.height = self.region_h
        else:
            self.height = self.image_max_height

    def _init_by_w_request(self):
        slice = self._strip_caret_if_upsample()
        self.width = int(slice[:-1])
        scale = self.width / self.region_w
        self.height = round(self.region_h * scale)

    def _init_by_h_request(self):
        slice = self._strip_caret_if_upsample()
        self.height = int(slice[1:])
        scale = self.height / self.region_h
        self.width = round(self.region_w * scale)

    def _init_by_pct_request(self):
        slice = self._strip_caret_if_upsample()
        try:
            scale = SizeParameter._pct_to_decimal(slice.split(":")[1])
        except ValueError as ve:
            raise SyntaxException(str(ve))
        if scale <= 0:
            msg = f"Size percentage must be greater than 0 ({self.uri_slice})."
            raise RequestException(msg)
        w_decimal = self.region_w * scale
        h_decimal = self.region_h * scale
        # handle teeny, tiny requests.
        self.width = 1 if 0 < w_decimal < 1 else int(w_decimal)
        self.height = 1 if 0 < h_decimal < 1 else int(h_decimal)

    def _init_by_confined_wh_request(self):
        slice = self._strip_caret_if_upsample()
        request_w, request_h = map(int, slice[1:].split(","))
        # TODO: below may need more precision than we get from floats w/
        # large images.
        scale = min(request_w / self.region_w, request_h / self.region_h)
        self.width = int(self.region_w * scale)
        self.height = int(self.region_h * scale)

    def _init_wh_request(self):
        slice = self._strip_caret_if_upsample()
        self.width, self.height = map(int, slice.split(","))

    def _strip_caret_if_upsample(self):
        s = self.uri_slice[1:] if self.upscaling_requested else self.uri_slice
        return s

    @staticmethod
    def _pct_to_decimal(n):
        return Decimal(float(n)) / DECIMAL_ONE_HUNDRED

    def _check_size_upscaling(self):
        upscaling_configured = FEATURE_SIZE_UPSCALING in self.enabled_features
        larger = self.width > self.region_w or self.height > self.region_h
        if self.upscaling_requested and not upscaling_configured:
            raise FeatureNotEnabledException(FEATURE_SIZE_UPSCALING)
        if larger and not self.upscaling_requested:
            msg = (
                f"Image would be upsampled (region is {self.region_w}×"
                f"{self.region_h}, image is {self.width}×{self.height}), but "
                "upsampling synax ('^') was not used."
            )
            raise RequestException(msg)

    def _check_if_supported(self):
        # raises FeatureNotEnabledException
        if self.request_type is KEYWORD_MAX:
            return
        try:
            if self.request_type not in self.enabled_features:
                raise FeatureNotEnabledException(self.request_type)
        except FeatureNotEnabledException as fe:
            if fe.feature is FEATURE_SIZE_BY_W and self._allowed_level0_size_request():
                return
            else:
                raise

    def _check_if_larger_than_max(self):
        area = self.width * self.height
        if self.info.max_area and area > self.info.max_area:
            msg = (
                f"Request area ({area}) is greater "
                f"than max area allowed ({self.info.max_area})"
            )
            raise RequestException(msg)
        if self.info.max_width and self.width > self.info.max_width:
            msg = (
                f"Request width ({self.width}) is greater than"
                f"max width allowed ({self.info.max_width})"
            )
            raise RequestException(msg)
        if self.info.max_height and self.height > self.info.max_height:
            msg = (
                f"Request height ({self.height}) is greater than"
                f"max height allowed ({self.info.max_height})"
            )
            raise RequestException(msg)

    def _allowed_level0_size_request(self):
        if self.info.tiles:
            tile_width = self.info.tiles[0].width
            tile_height = self.info.tiles[0].height
            right_col_width = self.info.width % tile_width
            bottom_row_height = self.info.height % tile_height
            tile_requirements = (
                self.width in (tile_width, right_col_width),
                self.height in (tile_height, bottom_row_height),
            )
            size = Size(self.width, self.height)
            return all(tile_requirements) or size in self.info.sizes
        else:
            return False
