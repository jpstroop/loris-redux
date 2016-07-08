from abc import ABCMeta
from abc import abstractmethod
from math import ceil

BITONAL_QUALITIES = ('bitonal',)
COLOR_QUALITIES = ('bitonal', 'color', 'gray')
GRAY_QUALITIES = ('bitonal', 'gray')

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
        # Must return a loris.info.data.InfoData object.
        return

    @classmethod
    def max_size(cls, image_width, image_height, max_area=None, max_width=None, max_height=None):
        # I stole this from @zimeon, sort of:
        w, h = image_width, image_height
        if max_area and max_area < (image_width * image_height):
            scale = (float(max_area) / float(image_width * image_height)) ** 0.5
            w, h = cls._scale_wh(scale, image_width, image_height)
        if max_width and max_width < w:
            scale = float(max_width) / float(image_width)
            w, h = cls._scale_wh(scale, image_width, image_height)
        if max_height and max_height < h:
            scale = float(max_height) / float(image_height)
            w, h = cls._scale_wh(scale, image_width, image_height)
        return cls._structure_size(w, h)

    @classmethod
    def _scale_wh(cls, scale, width, height):
        return [cls._scale_dim(d, scale) for d in (width, height)]

    @staticmethod
    def _scale_dim(dim, scale):
        return int(dim * scale + 0.5)

    @staticmethod
    def _structure_tiles(w, h, scales):
        d = { 'width' : w, 'scaleFactors' : scales }
        if w != h: d['height'] = h
        return [d]

    @classmethod
    def _structure_size(cls, w, h):
        return { 'width' : w, 'height' : h }
