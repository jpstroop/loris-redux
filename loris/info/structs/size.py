from collections import OrderedDict

from loris.constants import WIDTH
from loris.constants import HEIGHT

class Size(object):
    __slots__ = 'width', 'height'

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __lt__(self, other):
        return self.width < other.width

    def __le__(self, other):
        return self.width <= other.width

    def __eq__(self, other):
        return (self.width == other.width) and (self.height == other.height)

    def __ge__(self, other):
        return self.width >= other.width

    def __gt__(self, other):
        return self.width > other.width

    def __ne__(self, other):
        return (self.width != other.width) or (self.height != other.height)

    def to_dict(self):
        return OrderedDict(((WIDTH, self.width), (HEIGHT, self.height)))
