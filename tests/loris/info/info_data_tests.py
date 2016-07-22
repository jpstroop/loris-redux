from loris.info.info_data import InfoData
from loris.info.info_data import CONTEXT
from loris.info.info_data import PROTOCOL
from loris.compliance import Compliance
import pytest

@pytest.fixture()
def compliance(level2_plus_json):
    return Compliance(level2_plus_json)

HTTP_ID = 'https://example.edu/images/1234'

class TestInfoData(object):

    # Defaults and stuff set up w/ init
    def test__to_dict_has_context(self, compliance):
        info = InfoData(compliance, HTTP_ID)
        assert info._to_dict()['@context'] == CONTEXT

    def test__to_dict_has_identifier(self, compliance):
        info = InfoData(compliance, HTTP_ID)
        assert info._to_dict()['@id'] == HTTP_ID

    def test__to_dict_has_protocol(self, compliance):
        info = InfoData(compliance, HTTP_ID)
        assert info._to_dict()['protocol'] == PROTOCOL

    def test__to_dict_has_profile(self, compliance):
        info = InfoData(compliance, HTTP_ID)
        assert 'profile' in info._to_dict()

    def test_long_dim(self, compliance):
        info = InfoData(compliance, HTTP_ID)
        info.width = 42
        info.height = 21
        assert info.long_dim == 42

    def test_short_dim(self, compliance):
        info = InfoData(compliance, HTTP_ID)
        info.width = 42
        info.height = 21
        assert info.short_dim == 21

    # Perhaps More to come, though as a Plain Old Python Object most of the
    # functionality of this class gets tested with the extractors, for better
    # or worse...
