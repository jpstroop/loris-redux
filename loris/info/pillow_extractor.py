from loris.info.abstract_extractor import AbstractExtractor
from loris.info.abstract_extractor import BITONAL_QUALITIES
from loris.info.abstract_extractor import COLOR_QUALITIES
from loris.info.abstract_extractor import GRAY_QUALITIES
from loris.info.info_data import InfoData
from math import ceil
from PIL import Image

MODES_TO_QUALITIES = {
    '1': BITONAL_QUALITIES,
    'L': GRAY_QUALITIES,
    'LA': GRAY_QUALITIES,
    'P': GRAY_QUALITIES,
    'RGB': COLOR_QUALITIES,
    'RGBA': COLOR_QUALITIES,
    'CMYK': COLOR_QUALITIES,
    'YCbCr': COLOR_QUALITIES,
    'I': COLOR_QUALITIES,
    'F': COLOR_QUALITIES
}

COLOR_MODES = ('RGB', 'RGBA', 'CMYK', 'YCbCr', 'I', 'F')

class PillowExtractor(AbstractExtractor):
    # See comments in AbstractExtractor (in this module) for how this is
    # intended to work.

    def __init__(self, compliance, app_configs):
        super().__init__(compliance, app_configs)
        sf = app_configs['scale_factors']['other_formats']
        self.include_scale_factors = sf['enabled'] and compliance.level == 0
        if self.include_scale_factors:
            self.tile_w = sf['tile_width']
            self.tile_h = sf['tile_height']

    def extract(self, path, http_identifier):
        info_data = InfoData(self.compliance, http_identifier)
        pillow_image = Image.open(path)
        w, h = pillow_image.size
        info_data.width, info_data.height = (w, h)
        info_data.profile = self._make_profile(pillow_image)
        info_data.sizes = [
            PillowExtractor.max_size(w, h, max_area=self.max_area, \
                max_width=self.max_width, max_height=self.max_height)
        ]
        if self.include_scale_factors:
            tiles, sizes = self.level_zero_tiles_and_sizes(w, h, self.tile_w, self.tile_h)
            info_data.tiles = tiles
            info_data.sizes = info_data.sizes + sizes
        return info_data

    @staticmethod
    def is_color(pillow_image):
        return pillow_image.mode in COLOR_MODES

    def level_zero_tiles_and_sizes(self, image_w, image_h, tile_w, tile_h):
        # These are designed to work w/ OSd, hence ceil().
        if self.compliance.level == 0:
            tiles = PillowExtractor._level_zero_tiles(image_w, image_h, tile_w, tile_h)
            # there's always a chance that the default tile size is larger
            # than the image, so
            smallest_scale = 1
            if tiles is not None:
                smallest_scale = tiles[0]['scaleFactors'][-1]
            sizes = PillowExtractor._level_zero_sizes(smallest_scale, image_w, image_h)
            return (tiles, sizes)
        else:
            # Shouldn't happen, but just to remind ourselves...
            m = 'level_zero_tiles_and_sizes called, but server compliance is {0}'
            raise Exception(m.format(self.compliance.level))

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

    def _make_profile(self, pillow_image):
        include_color = PillowExtractor.is_color(pillow_image)
        profile = self.compliance.to_profile(include_color=include_color, \
            max_area=self.max_area, max_width=self.max_width, \
            max_height=self.max_height)
        return profile
