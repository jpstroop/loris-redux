from loris.compliance.format import FormatCompliance
from loris.compliance.helpers import ComparableMixin
from loris.compliance.helpers import st
from loris.compliance.http import HttpCompliance
from loris.compliance.quality import QualityCompliance
from loris.compliance.region import RegionCompliance
from loris.compliance.rotation import RotationCompliance
from loris.compliance.size import SizeCompliance
from loris.constants import COLOR
from loris.constants import MAX_AREA
from loris.constants import MAX_HEIGHT
from loris.constants import MAX_WIDTH


class Compliance(ComparableMixin):

    ALL_LEVEL_1 = st(
        HttpCompliance.LEVEL_1 +
        QualityCompliance.LEVEL_1 +
        RegionCompliance.LEVEL_1 +
        RotationCompliance.LEVEL_1 +
        SizeCompliance.LEVEL_1
    )

    ALL_LEVEL_2 = st(
        FormatCompliance.LEVEL_2 +
        HttpCompliance.LEVEL_2 +
        QualityCompliance.LEVEL_2 +
        RegionCompliance.LEVEL_2 +
        RotationCompliance.LEVEL_2 +
        SizeCompliance.LEVEL_2
    )

    def __init__(self, config):
        self.format = FormatCompliance(config['formats'])
        self.http = HttpCompliance(config['http'])
        self.quality = QualityCompliance(config['quality'])
        self.region = RegionCompliance(config['region'])
        self.rotation = RotationCompliance(config['rotation'])
        self.size = SizeCompliance(config['size'])

        self._additional_features = None
        self._int = None
        self._uri = None

    # make it possible to do int(self), and do comparisons
    def __int__(self):
        if self._int is None:
            ints = map(int, (self.format, self.http, self.quality,
                self.region, self.rotation, self.size) )
            self._int = min(ints)
        return self._int

    @property
    def uri(self):
        if self._uri is None:
            self._uri = f'http://iiif.io/api/image/3/level{int(self)}.json'
        return self._uri

    @property
    def all_enabled_features(self):
        # Note that formats and qualities aren't 'features' and are always
        # listed explicitly in the profile (other that jpg and default)
        return st(
            self.http.features +
            self.region.features +
            self.rotation.features +
            self.size.features
        )

    @property
    def additional_features(self):
        # Features supported above the calculated compliance level, i.e. the
        # difference between all enabled features and the calculated compliance
        # level. For listing in profile[1]['supports'].
        if self._additional_features is None:
            level_features = set(()) # 0
            if int(self) == 2:
                level_features = set(Compliance.ALL_LEVEL_2)
            elif int(self) == 1:
                level_features = set(Compliance.ALL_LEVEL_1)
            self._additional_features = set(self.all_enabled_features) - level_features
        return st(self._additional_features)

    def to_profile(self, **kwargs):
        # A tuple suitable for placing in the "supports" key of info.json
        # Pass include_color=False if the source image is grayscale. Can also
        # pass max_area, max_width, and max_height
        d = { }
        qualities = self.quality.features
        if not kwargs.get('include_color', True):
            qualities = tuple(filter(lambda q: q != COLOR, qualities))
        if qualities:
            d['qualities'] = qualities

        if self.additional_features:
            d['supports'] = self.additional_features
        if self.format.features:
            d['formats'] = self.format.features
        if kwargs.get('max_area') is not None:
            d[MAX_AREA] = kwargs['max_area']
        if kwargs.get('max_width') is not None:
            d[MAX_WIDTH] = kwargs['max_width']
        if kwargs.get('max_height') is not None:
            d[MAX_HEIGHT] = kwargs['max_height']
        return ( self.uri, d )
