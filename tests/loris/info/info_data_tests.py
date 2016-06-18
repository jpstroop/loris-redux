from loris.info.info_data import InfoData
from loris.info.info_data import CONTEXT
from loris.info.info_data import PROTOCOL
from loris.helpers.compliance import Compliance
import pytest

@pytest.fixture()
def compliance(level2_plus_json):
    return Compliance(level2_plus_json)

@pytest.fixture()
def http_id():
    return 'https://example.edu/images/1234'

class TestInfoData(object):

    # Defaults and stuff set up w/ init
    def test__to_dict_has_context(self, compliance, http_id):
        info = InfoData(compliance, http_id)
        assert info._to_dict()['@context'] == CONTEXT

    def test__to_dict_has_identifier(self, compliance, http_id):
        info = InfoData(compliance, http_id)
        assert info._to_dict()['@id'] == http_id

    def test__to_dict_has_protocol(self, compliance, http_id):
        info = InfoData(compliance, http_id)
        assert info._to_dict()['protocol'] == PROTOCOL

    def test__to_dict_has_profile(self, compliance, http_id):
        info = InfoData(compliance, http_id)
        assert 'profile' in info._to_dict()


    # More to come. Consider doing w/ Mocks to that we can keep serializtion
    # problems separate from extraction problems: https://pypi.python.org/pypi/pytest-mock/
