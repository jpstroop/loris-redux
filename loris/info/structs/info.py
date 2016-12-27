from collections import OrderedDict
from operator import methodcaller
import json

from loris.constants import CONTEXT
from loris.constants import PROTOCOL

class Info(object):
    # POPO for info.json
    __slots__ = (
        'identifier',
        'compliance',
        'width',
        'height',
        'tiles',
        'sizes',
        'profile',
        'color_profile_bytes',
        '_long_dim',
        '_short_dim',
        '_all_scales'
    )

    def __init__(self, compliance, http_identifier):
        self.identifier = http_identifier
        self.compliance = compliance
        self.width = None
        self.height = None
        self.tiles = None
        self.sizes = None
        self.profile = None
        self.color_profile_bytes = None
        self._long_dim = None
        self._short_dim = None
        self._all_scales = None

    def __str__(self):
        return json.dumps(self.to_dict())

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

    def to_dict(self):
        d = OrderedDict()
        d['@context'] = CONTEXT
        d['@id'] = self.identifier
        d['protocol'] = PROTOCOL
        d['profile'] = self.profile
        d['width'] = self.width
        d['height'] = self.height
        if self.tiles:
            d['tiles'] =  list(map(methodcaller('to_dict'), sorted(self.tiles)))
        if self.sizes:
            d['sizes'] = list(map(methodcaller('to_dict'), sorted(self.sizes)))
        return d
