from loris.info.abstract_extractor import AbstractExtractor
from loris.info.abstract_extractor import BITONAL_QUALITIES
from loris.info.abstract_extractor import COLOR_QUALITIES
from loris.info.abstract_extractor import GRAY_QUALITIES
from loris.info.info_data import InfoData
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
        # TODO: This still feels messy. Refactor (and push up to abstract?)
        if self.level_0_scale_factors_enabled:
            tiles, sizes = self.level_zero_tiles_and_sizes(w, h, self.level0_tile_w, self.level0_tile_h)
            info_data.tiles = tiles
            info_data.sizes = info_data.sizes + sizes
        return info_data

    @staticmethod
    def is_color(pillow_image):
        return pillow_image.mode in COLOR_MODES

    def _make_profile(self, pillow_image):
        include_color = PillowExtractor.is_color(pillow_image)
        return self.compliance.to_profile(include_color=include_color)
