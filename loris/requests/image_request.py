from loris.parameters.format import FormatParameter
from loris.parameters.quality import QualityParameter
from loris.parameters.region import RegionParameter
from loris.parameters.rotation import RotationParameter
from loris.parameters.size import SizeParameter
from loris.requests.iiif_request import IIIFRequest

from hashlib import sha1

class ImageRequest(IIIFRequest):

    def __init__(self, identifier, iiif_params):
        super().__init__(identifier, iiif_params)
        region_s, size_s, rotation_s, quality_fmt = iiif_params.split('/')
        quality_s, format_s = quality_fmt.split('.')

        self.region_param = self._init_region(region_s)
        self.size_param = self._init_size(size_s)
        self.rotation_param = self._init_rotation(rotation_s)
        self.quality_param = self._init_quality(quality_s)
        self.format_param = self._init_format(format_s)
        self._canonical = None

    @property
    def canonical(self):
        if self._canonical is None:
            params = (
                self.region_param.canonical,
                self.size_param.canonical,
                self.rotation_param.canonical,
                self.quality_param.canonical
            )
            path = '/'.join(map(str, params)) # str(param) returns the canonical version
            self._canonical = '{0}.{1}'.format(path, self.format_param.canonical)
        return self._canonical

    @property
    def etag(self):
        if self._etag is None:
            last_mod = str(self.last_mod)
            b = bytes(last_mod + self.file_path + self.canonical, 'utf-8')
            self._etag = sha1(b).hexdigest()
        return self._etag

    def _init_region(self, region):
        # Should probably wrap IIIFRequest.compliance.region.features
        # as IIIFRequest.enabled_region_features, but not sure if all of this
        # should be part of the IIIFRequest class, so leaving for now.
        enabled_features = IIIFRequest.compliance.region.features
        return RegionParameter(region, enabled_features, self.info)

    def _init_size(self, size):
        enabled_features = IIIFRequest.compliance.size.features
        return SizeParameter(size, enabled_features, self.info, self.region_param)

    def _init_rotation(self, rotation):
        enabled_features = IIIFRequest.compliance.rotation.features
        return RotationParameter(rotation, enabled_features)

    def _init_quality(self, quality):
        enabled_features = IIIFRequest.compliance.quality.features
        return QualityParameter(quality, enabled_features, self.info)

    def _init_format(self, fmt):
        enabled_features = IIIFRequest.compliance.format.features
        return FormatParameter(fmt, enabled_features, self.info)
