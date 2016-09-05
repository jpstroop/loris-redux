from loris.parameters.format import FormatParameter
from loris.parameters.quality import QualityParameter
from loris.parameters.region import RegionParameter
from loris.parameters.rotation import RotationParameter
from loris.parameters.size import SizeParameter
from hashlib import sha1
from operator import methodcaller
from os import stat

class ImageRequest(object):
    __slots__ = (
        'file_path',
        'info',
        'compliance',
        'region_param',
        'size_param',
        'rotation_param',
        'quality_param',
        'format_param',
        '_canonical',
        '_etag'

    )

    def __init__(self, file_path, iiif_params, compliance, info):
        region_s, size_s, rotation_s, quality_fmt = iiif_params.split('/')
        quality_s, format_s = quality_fmt.split('.')

        self.file_path = file_path
        self.info = info
        self.compliance = compliance
        self.region_param = self._init_region(region_s)
        self.size_param = self._init_size(size_s)
        self.rotation_param = self._init_rotation(rotation_s)
        self.quality_param = self._init_quality(quality_s)
        self.format_param = self._init_format(format_s)
        self._canonical = None
        self._etag = None

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

    @property # TODO: info requests might be able to use this as well (superclass or mixin?)
    def etag(self):
        if self._etag is None:
            last_mod = str(stat(self.file_path).st_mtime)
            b = bytes(last_mod + self.file_path + self.canonical, 'utf-8')
            self._etag = sha1(b).hexdigest()
        return self._etag

    def _init_region(self, region):
        enabled_features = self.compliance.region.features
        return RegionParameter(region, enabled_features, self.info)

    def _init_size(self, size):
        enabled_features = self.compliance.size.features
        return SizeParameter(size, enabled_features, self.info, self.region_param)

    def _init_rotation(self, rotation):
        enabled_features = self.compliance.rotation.features
        return RotationParameter(rotation, enabled_features)

    def _init_quality(self, quality):
        enabled_features = self.compliance.quality.features
        return QualityParameter(quality, enabled_features, self.info)

    def _init_format(self, fmt):
        enabled_features = self.compliance.format.features
        return FormatParameter(fmt, enabled_features, self.info)
