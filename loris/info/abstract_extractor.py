from abc import ABCMeta
from abc import abstractmethod
from loris.constants import QUALITY_BITONAL_QUALITIES
from loris.constants import COLOR_QUALITIES
from loris.info.structs.info import Info
from loris.info.structs.size import Size
from math import ceil

class AbstractExtractor(metaclass=ABCMeta):
    #
    # The InfoHandler has a static dict of these, one for each format we
    # support, e.g., at init:
    #
    # extractors = { 'jp2' : jp2extractor_instance, 'jpg' : ... }
    #
    # and then, for each request, the InfoHandler instance does something like:
    #
    # path, format = resolver.resvolve(identifier)
    # http_identifier = server_uri + urllib.quote_plus(identifier # accounting for trailing /
    # info = extractors[format].extract(path, http_identifier)
    #
    def __init__(self, compliance, app_configs):
        self.compliance = compliance
        self.app_configs = app_configs
        self._max_area = self.app_configs.get('max_area')
        self._max_width = self.app_configs.get('max_width')
        self._max_height = self.app_configs.get('max_height')

    def init_info(self, http_identifier):
        # This is all of the info that is per-server
        info = Info(self.compliance, http_identifier)
        info.extra_features = self.compliance.extra_features
        info.extra_formats = self.compliance.extra_formats
        info.max_area = self._max_area
        info.max_width = self._max_width
        info.max_height = self._max_height
        return info

    @abstractmethod
    def extract(self, path, http_identifier):  # pragma: no cover
        # Must return a loris.info.data.Info object.
        return

    def max_size(self, image_width, image_height):
        w, h = image_width, image_height
        if self._max_area and self._max_area < (w * h):
            scale = (self._max_area / (image_width * image_height)) ** 0.5
            w, h = AbstractExtractor._scale_wh(scale, image_width, image_height)
        if self._max_width and self._max_width < w:
            scale = self._max_width / image_width
            w, h = AbstractExtractor._scale_wh(scale, image_width, image_height)
        if self._max_height and self._max_height < h:
            scale = self._max_height / image_height
            w, h = AbstractExtractor._scale_wh(scale, image_width, image_height)
        return Size(w, h)

    @staticmethod
    def _scale_wh(scale, width, height):
        return [AbstractExtractor._scale_dim(d, scale) for d in (width, height)]

    @staticmethod
    def _scale_dim(dim, scale):
        return int(dim * scale + 0.5)
