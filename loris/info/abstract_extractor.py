from abc import ABCMeta
from abc import abstractmethod
from math import ceil

from loris.constants import BITONAL_QUALITIES
from loris.constants import COLOR_QUALITIES
from loris.constants import GRAY_QUALITIES
from loris.info.structs.size import Size

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
        self.max_area = app_configs['max_area']
        self.max_width = app_configs['max_width']
        self.max_height = app_configs['max_height']

    @abstractmethod
    def extract(self, path, http_identifier):  # pragma: no cover
        # Must return a loris.info.data.Info object.
        return

    @classmethod
    def max_size(cls, image_width, image_height, max_area=None, max_width=None, max_height=None):
        # I stole this from @zimeon, sort of:
        w, h = image_width, image_height
        if max_area and max_area < (image_width * image_height):
            scale = (max_area / (image_width * image_height)) ** 0.5
            w, h = cls._scale_wh(scale, image_width, image_height)
        if max_width and max_width < w:
            scale = max_width / image_width
            w, h = cls._scale_wh(scale, image_width, image_height)
        if max_height and max_height < h:
            scale = max_height / image_height
            w, h = cls._scale_wh(scale, image_width, image_height)
        return Size(w, h)

    @classmethod
    def _scale_wh(cls, scale, width, height):
        return [cls._scale_dim(d, scale) for d in (width, height)]

    @staticmethod
    def _scale_dim(dim, scale):
        return int(dim * scale + 0.5)
