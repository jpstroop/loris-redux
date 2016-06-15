import json

PROTOCOL = 'http://iiif.io/api/image'
CONTEXT = 'http://iiif.io/api/image/2/context.json'

class InfoData(object):
    # POPO for info.json
    def __init__(self, compliance, http_identifier):
        self.identifier = http_identifier
        self.is_color = False
        self.compliance = compliance
        self.width = None
        self.height = None
        self.tiles = None
        self.sizes = None

    def to_json(self):
        return json.dumps(self._to_dict())

    def _to_dict(self):
        d = {}
        d['@context'] = CONTEXT
        d['@id'] = self.identifier
        d['protocol'] = PROTOCOL
        d['profile'] = self.compliance.to_profile(include_color=self.is_color)
        d['width'] = self.width
        d['height'] = self.height
        if self.tiles:
            d['tiles'] = self.tiles
        if self.sizes:
            d['sizes'] = self.sizes
        return d
