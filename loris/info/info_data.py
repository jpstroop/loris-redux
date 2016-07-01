from collections import OrderedDict
import json

PROTOCOL = 'http://iiif.io/api/image'
CONTEXT = 'http://iiif.io/api/image/2/context.json'

class InfoData(object):
    # POPO for info.json
    def __init__(self, compliance, http_identifier):
        self.identifier = http_identifier
        self.compliance = compliance
        self.width = None
        self.height = None
        self.tiles = None
        self.sizes = None
        self.profile = None
        self.color_profile_bytes = None

    def __str__(self):
        return json.dumps(self._to_dict())

    def __repr__(self):
        return repr(self._to_dict())

    def _to_dict(self):
        d = OrderedDict()
        d['@context'] = CONTEXT
        d['@id'] = self.identifier
        d['protocol'] = PROTOCOL
        d['profile'] = self.profile
        d['width'] = self.width
        d['height'] = self.height
        if self.tiles:
            d['tiles'] = self.tiles
        if self.sizes:
            d['sizes'] = self.sizes
        return d
