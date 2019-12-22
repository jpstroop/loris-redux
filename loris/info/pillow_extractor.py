from math import ceil
from PIL import Image

from loris.constants import QUALITY_BITONAL_QUALITIES
from loris.constants import COLOR_QUALITIES
from loris.constants import QUALITY_GROUP_GRAY
from loris.info.abstract_extractor import AbstractExtractor
from loris.info.structs.info import Info
from loris.info.structs.size import Size
from loris.info.structs.tile import Tile

MODES_TO_QUALITIES = {
    '1': QUALITY_BITONAL_QUALITIES,
    'L': QUALITY_GROUP_GRAY,
    'LA': QUALITY_GROUP_GRAY,
    'P': QUALITY_GROUP_GRAY,
    'RGB': COLOR_QUALITIES,
    'RGBA': COLOR_QUALITIES,
    'CMYK': COLOR_QUALITIES,
    'YCbCr': COLOR_QUALITIES,
    'I': COLOR_QUALITIES,
    'F': COLOR_QUALITIES
}

COLOR_MODES = ('RGB', 'RGBA', 'CMYK', 'YCbCr', 'I', 'F')

class PillowExtractor(AbstractExtractor):

    def __init__(self, compliance, app_configs):
        super().__init__(compliance, app_configs)
        sf = app_configs['sizes_and_tiles']['other_formats']
        self.include_sizes_and_tiles = sf['enabled']
        if self.include_sizes_and_tiles:
            self.tile_w = sf['tile_width']
            self.tile_h = sf['tile_height']
            self.include_all_factors = sf['all_scale_factors']
            self.min_dimension = sf['min_dimension']

    def extract(self, path, http_identifier):
        info = self.init_info(http_identifier)
        pillow_image = Image.open(path)
        w, h = pillow_image.size
        info.width, info.height = (w, h)
        info.extra_qualities = self._make_qualities(pillow_image)
        max_size = self.max_size(w, h)
        if self.include_sizes_and_tiles:
            scale_factors = self._scale_factors(w, h)
            info.tiles = self._calc_tiles(w, h, scale_factors)
            tile_size = info.tiles[0]
            info.sizes = self._calc_sizes(w, h, max_size, tile_size, scale_factors)
        else:
            info.sizes = [max_size]
        return info

    def _make_qualities(self, pillow_image):
        is_color = PillowExtractor.is_color(pillow_image)
        return self.compliance.extra_qualities(is_color)

    def _scale_factors(self, image_w, image_h):
        short_image_dimenson = min(image_w, image_h)
        scales = []
        nxt = 1
        while ceil(short_image_dimenson / nxt) >= self.min_dimension:
            scales.append(nxt)
            nxt = scales[-1]*2
        return scales

    def _calc_tiles(self, image_w, image_h, scale_factors):
        image_long = max(image_w, image_h)
        self.tile_long =  max(self.tile_w, self.tile_h)
        scales = filter(lambda s: (image_long / s) > self.tile_long, scale_factors)
        return [ Tile(self.tile_w, tuple(scales), self.tile_h) ]

    def _calc_sizes(self, image_w, image_h, max_size, tile_size, scale_factors):
        # Note: We make heavy use of the fact that Size and Tile structs are
        # comparable here. See loris.info.structs.size.Size, etc. for details.
        # It's cool.
        sizes = [ max_size ]
        for s in scale_factors:
            this_size = Size(ceil(image_w / s), ceil(image_h / s))
            less_than_max = this_size < max_size
            less_than_tile = this_size < tile_size
            if self.include_all_factors and less_than_max:
                sizes.append(this_size)
            elif not self.include_all_factors and less_than_tile:
                sizes.append(this_size)
        return sizes

    @staticmethod
    def is_color(pillow_image):
        return pillow_image.mode in COLOR_MODES
