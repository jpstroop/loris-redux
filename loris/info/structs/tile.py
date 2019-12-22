from loris.info.structs.size import Size
from loris.constants import KEYWORD_HEIGHT
from loris.constants import KEYWORD_SCALE_FACTORS

class Tile(Size):
    __slots__ = 'scale_factors'

    def __init__(self, width, scale_factors, height=None):
        self.width = width
        self.height = height if height is not None else width
        self.scale_factors = scale_factors

    def to_dict(self):
        d = super().to_dict()
        if self.width == self.height:
            del d[KEYWORD_HEIGHT]
        d[KEYWORD_SCALE_FACTORS] = self.scale_factors
        return d
