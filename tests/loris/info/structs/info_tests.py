from loris.info.structs.info import Info
from loris.compliance import Compliance
from loris.constants import CONTEXT
from loris.constants import PROTOCOL
from loris.info.structs.size import Size
from loris.info.structs.tile import Tile
from collections import OrderedDict
import pytest

@pytest.fixture()
def compliance(level2_plus_json):
    return Compliance(level2_plus_json)

HTTP_ID = 'https://example.edu/images/1234'

class TestInfo(object):

    # Defaults and stuff set up w/ init
    def test_to_dict_has_context(self, compliance):
        info = Info(compliance, HTTP_ID)
        assert info.to_dict()['@context'] == CONTEXT

    def test_to_dict_has_identifier(self, compliance):
        info = Info(compliance, HTTP_ID)
        assert info.to_dict()['@id'] == HTTP_ID

    def test_to_dict_has_protocol(self, compliance):
        info = Info(compliance, HTTP_ID)
        assert info.to_dict()['protocol'] == PROTOCOL

    def test_to_dict_has_profile(self, compliance):
        info = Info(compliance, HTTP_ID)
        assert 'profile' in info.to_dict()

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
