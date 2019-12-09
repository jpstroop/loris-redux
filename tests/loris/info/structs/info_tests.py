from collections import OrderedDict
from loris.compliance import Compliance
from loris.constants import CONTEXT
from loris.constants import CONTEXT_URI
from loris.constants import ID
from loris.constants import IMAGE_SERVICE_3
from loris.constants import MAX_AREA
from loris.constants import PROTOCOL
from loris.constants import PROTOCOL_URI
from loris.constants import TYPE
from loris.info.structs.info import Info
from loris.info.structs.size import Size
from loris.info.structs.tile import Tile
import pytest

@pytest.fixture()
def compliance(level2_plus_yaml):
    return Compliance(level2_plus_yaml)

HTTP_ID = 'https://example.edu/images/1234'

class TestInfo(object):

    # Defaults and stuff set up w/ init
    def test_dict_has_boilerplate_values(self, compliance):
        info = Info(compliance, HTTP_ID)
        d = info.to_dict()
        assert d[CONTEXT] == CONTEXT_URI
        assert d[PROTOCOL] == PROTOCOL_URI
        assert d[TYPE] == IMAGE_SERVICE_3
        assert d[ID] == HTTP_ID

    def test_to_dict_strips_none_values(self, compliance):
        info = Info(compliance, HTTP_ID)
        info.max_area = None
        d = info.to_dict()
        assert MAX_AREA not in d

    def test_long_dim(self, compliance):
        info = Info(compliance, HTTP_ID)
        info.width = 42
        info.height = 21
        assert info.long_dim == 42

    def test_short_dim(self, compliance):
        info = Info(compliance, HTTP_ID)
        info.width = 42
        info.height = 21
        assert info.short_dim == 21

    def test_sizes_sort_in_to_dict(self, compliance):
        # Integrates w/ Size. If this is failing, check Size first
        info = Info(compliance, HTTP_ID)
        s1 = Size(1500, 750)
        s2 = Size(3000, 1500)
        s3 = Size(6000, 3000)
        info.sizes = [s2, s3, s1]
        expected = [
            OrderedDict([('width', 1500), ('height', 750)]),
            OrderedDict([('width', 3000), ('height', 1500)]),
            OrderedDict([('width', 6000), ('height', 3000)])
        ]
        assert info.to_dict()['sizes'] == expected

    def test_tiles_sort_in_to_dict(self, compliance):
        # Integrates w/ Tile. If this is failing, check Size first
        info = Info(compliance, HTTP_ID)
        t1 = Tile(512, [1, 2, 4])
        t2 = Tile(1024, [8], 2048)
        t3 = Tile(2048, [16])
        info.tiles = [t2, t3, t1]
        expected = [
            OrderedDict([('width', 512), ('scaleFactors', [1, 2, 4])]),
            OrderedDict([
                ('width', 1024),
                ('height', 2048),
                ('scaleFactors', [8])
            ]),
            OrderedDict([('width', 2048), ('scaleFactors', [16])])
        ]
        assert info.to_dict()['tiles'] == expected

    def test_all_scales(self, compliance):
        # Integrates w/ Tile. If this is failing, check Size first
        info = Info(compliance, HTTP_ID)
        t1 = Tile(512, [1, 2, 4])
        t2 = Tile(1024, [8], 2048)
        t3 = Tile(2048, [16])
        info.tiles = [t1, t2, t3]
        assert info.all_scales == [1, 2, 4, 8, 16]
