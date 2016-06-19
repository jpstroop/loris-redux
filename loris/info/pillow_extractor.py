from loris.info.extract_api import AbstractExtractor
from loris.info.extract_api import BITONAL_QUALITIES
from loris.info.extract_api import COLOR_QUALITIES
from loris.info.extract_api import GRAY_QUALITIES
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
    # TODO: needs configured values for maxWidth, maxHeight...
    def __init__(self, compliance, app_configs):
        super().__init__(compliance, app_configs)

    def extract(self, path, http_identifier):
        # TODO: maxArea, maxWidth, maxHeight
        info_data = InfoData(self.compliance, http_identifier)
        pillow_image = Image.open(path)
        info_data.width, info_data.height = pillow_image.size
        info_data.profile = self._make_profile(pillow_image)
        return info_data

    def _make_profile(self, pillow_image):
        include_color = PillowExtractor.is_color(pillow_image)
        return self.compliance.to_profile(include_color=include_color)

    @staticmethod
    def is_color(pillow_image):
        return pillow_image.mode in COLOR_MODES

    # TODO: sizes / tiles
    def _level_zero_sizes(image_w, image_h, tile_w, tile_h):
        # start w/ values from self.compliance
        pass
