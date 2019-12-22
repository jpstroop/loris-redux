from collections import OrderedDict
from dataclasses import dataclass
from json import dumps
from loris.compliance import Compliance
from loris.constants import KEYWORD_CONTEXT
from loris.constants import KEYWORD_EXTRA_FEATURES
from loris.constants import KEYWORD_EXTRA_FORMATS
from loris.constants import KEYWORD_EXTRA_QUALITIES
from loris.constants import KEYWORD_HEIGHT
from loris.constants import KEYWORD_ID
from loris.constants import KEYWORD_IMAGE_SERVICE_3
from loris.constants import KEYWORD_MAX_AREA
from loris.constants import KEYWORD_MAX_HEIGHT
from loris.constants import KEYWORD_MAX_WIDTH
from loris.constants import KEYWORD_PROFILE
from loris.constants import KEYWORD_PROTOCOL
from loris.constants import KEYWORD_SIZES
from loris.constants import KEYWORD_TILES
from loris.constants import KEYWORD_TYPE
from loris.constants import KEYWORD_WIDTH
from loris.constants import URI_CONTEXT
from loris.constants import URI_PROTOCOL
from loris.info.structs.size import Size
from loris.info.structs.tile import Tile
from operator import methodcaller
from typing import List

@dataclass
class Info:
    compliance: Compliance  # These are by the
    http_identifier: str    # required contructor
    width: int = None
    height: int = None
    _long_dim: int = None
    _short_dim: int = None
    _all_scales:  List[int] = None
    tiles: List[Tile] = None
    sizes: List[Size] = None
    max_area: int = None
    max_width: int = None
    max_height: int = None
    extra_formats: List[str] = None
    extra_qualities: List[str] = None
    extra_features: List[str] = None

    def __str__(self):
        return dumps(self.to_dict())

    def __repr__(self):
        return repr(self.to_dict())

    @property
    def long_dim(self):
        if not self._long_dim:
            self._long_dim =  max(self.width, self.height)
        return self._long_dim

    @property
    def short_dim(self):
        if not self._short_dim:
            self._short_dim =  min(self.width, self.height)
        return self._short_dim

    @property
    def all_scales(self):
        # When dealing with Jp2s, scaleFactors are the same as the baked-in
        # resolutions. These are easier to deal with than the sizes list when
        # making derivatives
        if not self._all_scales:
            self._all_scales = [s for t in self.tiles for s in t.scale_factors]
        return self._all_scales

    @staticmethod
    def _cleandict(d):
        '''
        Remove None values from the dict to avoid nulls in serialization.
        '''
        if not isinstance(d, OrderedDict):
            return d
        return (
            { k : Info._cleandict(v) for (k,v) in d.items() if v is not None }
        )

    def to_dict(self):
        d = OrderedDict()
        d[KEYWORD_CONTEXT] = URI_CONTEXT
        d[KEYWORD_ID] = self.http_identifier
        d[KEYWORD_TYPE] = KEYWORD_IMAGE_SERVICE_3
        d[KEYWORD_PROTOCOL] = URI_PROTOCOL
        d[KEYWORD_PROFILE] = str(self.compliance)
        d[KEYWORD_WIDTH] = self.width
        d[KEYWORD_HEIGHT] = self.height
        if self.tiles:
            d[KEYWORD_TILES] =  list(map(methodcaller('to_dict'), sorted(self.tiles)))
        if self.sizes:
            d[KEYWORD_SIZES] = list(map(methodcaller('to_dict'), sorted(self.sizes)))
        d[KEYWORD_MAX_AREA] = self.max_area
        d[KEYWORD_MAX_WIDTH] = self.max_width
        d[KEYWORD_MAX_HEIGHT] = self.max_height
        d[KEYWORD_EXTRA_FORMATS] = self.extra_formats
        d[KEYWORD_EXTRA_QUALITIES] = self.extra_qualities
        d[KEYWORD_EXTRA_FEATURES] = self.extra_features
        return Info._cleandict(d)
