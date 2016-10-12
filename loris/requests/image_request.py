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

        self._region_param = self._init_region(region_s)
        self._size_param = self._init_size(size_s)
        self._rotation_param = self._init_rotation(rotation_s)
        self._quality_param = self._init_quality(quality_s)
        self._format_param = self._init_format(format_s)
        self._init_delegations()
        self._canonical = None

    def _init_delegations(self):
        # This makes mocking a TON easier, plus Law of Demeter, whatever...
        self.region_request_type = self._region_param.request_type
        self.region_decimal_x = self._region_param.decimal_x
        self.region_decimal_y = self._region_param.decimal_y
        self.region_decimal_w = self._region_param.decimal_w
        self.region_decimal_h = self._region_param.decimal_h
        self.region_pixel_x = self._region_param.pixel_x
        self.region_pixel_y = self._region_param.pixel_y
        self.region_pixel_w = self._region_param.pixel_w
        self.region_pixel_h = self._region_param.pixel_h
        self.size_request_type = self._size_param.request_type
        self.width = self._size_param.width
        self.height = self._size_param.height
        self.mirror = self._rotation_param.mirror
        self.rotation = self._rotation_param.rotation
        self.quality = self._quality_param.canonical
        self.format = self._format_param.canonical

    @property
    def canonical(self):
        if self._canonical is None:
            params = (
                self._region_param,
                self._size_param,
                self._rotation_param,
                self._quality_param
            )
            path = '/'.join(map(str, params)) # str(param) returns the canonical version
            self._canonical = '{0}.{1}'.format(path, self.format)
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
        return SizeParameter(size, enabled_features, self.info, self._region_param)

    def _init_rotation(self, rotation):
        enabled_features = IIIFRequest.compliance.rotation.features
        return RotationParameter(rotation, enabled_features)

    def _init_quality(self, quality):
        enabled_features = IIIFRequest.compliance.quality.features
        return QualityParameter(quality, enabled_features, self.info)

    def _init_format(self, fmt):
        enabled_features = IIIFRequest.compliance.format.features
        return FormatParameter(fmt, enabled_features, self.info)
