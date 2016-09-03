from loris.info.structs.size import Size
from collections import OrderedDict

class TestSize(object):

    def test_sorts_by_width_ascending(self):
        s1 = Size(1500, 750)
        s2 = Size(3000, 1500)
        s3 = Size(6000, 3000)
        assert sorted([s2, s3, s1]) == [s1, s2, s3]

    def test_to_dict(self):
        s = Size(1500, 750)
        expected = OrderedDict([('width', 1500), ('height', 750)])
        assert s.to_dict() == expected
