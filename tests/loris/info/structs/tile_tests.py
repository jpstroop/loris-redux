from loris.info.structs.tile import Tile
from collections import OrderedDict

class TestTile(object):

    def test_sorts_by_width_ascending(self):
        t1 = Tile(512, [1, 2, 4])
        t2 = Tile(1024, [8])
        t3 = Tile(2048, [16])
        assert sorted([t2, t3, t1]) == [t1, t2, t3]

    def test_height_defaults_to_width(self):
        t = Tile(512, [1, 2, 4])
        assert t.height == 512

    def test_height_can_be_different(self):
        t = Tile(512, [1, 2, 4], 1024)
        assert t.height == 1024

    def test_to_dict(self):
        t = Tile(2048, [8, 16])
        expected = OrderedDict([('width', 2048), ('scaleFactors', [8, 16])])
        assert t.to_dict() == expected

    def test_to_dict_with_height(self):
        t = Tile(2048, [8, 16], 1024)
        expected = OrderedDict([
            ('width', 2048),
            ('height', 1024),
            ('scaleFactors', [8, 16])
        ])
        assert t.to_dict() == expected
