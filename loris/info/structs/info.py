from collections import OrderedDict
from dataclasses import dataclass
from json import dumps
from loris.compliance import Compliance
from loris.constants import CONTEXT
from loris.constants import CONTEXT_URI
from loris.constants import EXTRA_FEATURES
from loris.constants import EXTRA_FORMATS
from loris.constants import EXTRA_QUALITIES
from loris.constants import HEIGHT
from loris.constants import ID
from loris.constants import IMAGE_SERVICE_3
from loris.constants import MAX_AREA
from loris.constants import MAX_HEIGHT
from loris.constants import MAX_WIDTH
from loris.constants import PROFILE
from loris.constants import PROTOCOL
from loris.constants import PROTOCOL_URI
from loris.constants import SIZES
from loris.constants import TILES
from loris.constants import TYPE
from loris.constants import WIDTH
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
        d[CONTEXT] = CONTEXT_URI
        d[ID] = self.http_identifier
        d[TYPE] = IMAGE_SERVICE_3
        d[PROTOCOL] = PROTOCOL_URI
        d[PROFILE] = str(self.compliance)
        d[WIDTH] = self.width
        d[HEIGHT] = self.height
        if self.tiles:
            d[TILES] =  list(map(methodcaller('to_dict'), sorted(self.tiles)))
        if self.sizes:
            d[SIZES] = list(map(methodcaller('to_dict'), sorted(self.sizes)))
        d[MAX_AREA] = self.max_area
        d[MAX_WIDTH] = self.max_width
        d[MAX_HEIGHT] = self.max_height
        d[EXTRA_FORMATS] = self.extra_formats
        d[EXTRA_QUALITIES] = self.extra_qualities
        d[EXTRA_FEATURES] = self.extra_features
        return Info._cleandict(d)
