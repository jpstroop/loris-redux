from abc import ABCMeta
from abc import abstractmethod
from math import ceil

BITONAL_QUALITIES = ('bitonal', 'default')
COLOR_QUALITIES = ('bitonal', 'color', 'default', 'gray')
GRAY_QUALITIES = ('bitonal', 'default', 'gray')

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
        sf = app_configs['scale_factors']
        self.level_0_scale_factors_enabled = sf.get('enabled', False) \
            and compliance.level == 0
        if self.level_0_scale_factors_enabled:
            self.level0_tile_w = sf['tile_width']
            self.level0_tile_h = sf.get('tile_height', self.level0_tile_w)
        self.max_area = app_configs.get('max_area')
        self.max_width = app_configs.get('max_width')
        self.max_height = app_configs.get('max_height')


    @abstractmethod
    def extract(self, path, http_identifier):  # pragma: no cover
        # Must return a loris.info.data.InfoData object.
        return

    # TODO: needs a size for full or max ... configured values for maxWidth, maxHeight...

    def level_zero_tiles_and_sizes(self, image_w, image_h, tile_w, tile_h):
        # These are designed to work w/ OSd, hence ceil().
        if self.compliance.level == 0:
            tiles = AbstractExtractor._level_zero_tiles(image_w, image_h, tile_w, tile_h)
            smallest_scale = tiles[0]['scaleFactors'][-1]
            sizes = AbstractExtractor._level_zero_sizes(smallest_scale, image_w, image_h)
            return (tiles, sizes)
        else:
            # Shouldn't happen, but just to remind ourselves...
            m = 'level_zero_tiles_and_sizes called, but server compliance is {0}'
            raise Exception(m.format(self.compliance.level))

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

    @classmethod
    def _level_zero_tiles(cls, image_w, image_h, tile_w, tile_h):
        long_image_dimenson = max(image_w, image_h)
        long_tile_dimenson =  max(tile_w, tile_h)
        scales = [1]
        while (long_image_dimenson / scales[-1]) > long_tile_dimenson:
            nxt = scales[-1]*2
            if (long_image_dimenson / nxt) > long_tile_dimenson:
                scales.append(nxt)
            else:
                return cls._structure_tiles(tile_w, tile_h, scales)

    @staticmethod
    def _structure_tiles(w, h, scales):
        d = { 'width' : w, 'scaleFactors' : scales }
        if w != h: d['height'] = h
        return [d]

    @classmethod
    def _structure_size(cls, w, h):
        return { 'width' : w, 'height' : h }

    @classmethod
    def _level_zero_sizes(cls, smallest_scale_factor, image_w, image_h):
        # smallest_scale_factor is tiles[0]['scaleFactors'][-1]
        sizes = [ ]
        scale = smallest_scale_factor*2
        w = ceil(image_w / scale)
        h = ceil(image_h / scale)
        while any([d != 1 for d in (w,h)]):
            sizes.append(cls._structure_size(w, h))
            scale = scale*2
            w = ceil(image_w / scale)
            h = ceil(image_h / scale)
        return sizes
