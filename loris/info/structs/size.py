from collections import OrderedDict
from dataclasses import dataclass
from loris.constants import KEYWORD_HEIGHT
from loris.constants import KEYWORD_WIDTH


@dataclass
class Size:
    __slots__ = "width", "height"
    width: int
    height: int

    def __lt__(self, other):
        return self.width < other.width and self.height < other.height

    def __le__(self, other):
        return self.width <= other.width and self.height <= other.height

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height

    def __ge__(self, other):
        return self.width >= other.width and self.height >= other.height

    def __gt__(self, other):
        return self.width > other.width and self.height > other.height

    def __ne__(self, other):
        return (self.width != other.width) or (self.height != other.height)

    def __repr__(self):
        return f"Size({self.width},{self.height})"

    def to_dict(self):
        return OrderedDict(((KEYWORD_WIDTH, self.width), (KEYWORD_HEIGHT, self.height)))
