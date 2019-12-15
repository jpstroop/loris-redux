from loris.constants import BASE_URI_REDIRECT
from loris.requests.info_request import IIIFRequest
from tests.loris.handlers.base_handler_test import BaseHandlerTest

class TestIdentifierHandler(BaseHandlerTest):
    def test_base_id_redirects(self):
        response = self.get("/nir%2fvana", allow_redirects=False)
        assert response.status_code == 303
        assert response.headers["Location"] == "/nir%2Fvana/info.json"

    def test_base_id_204_if_redirect_disabled(self):
        IIIFRequest.compliance.http.features = ()
        response = self.get("/nir%2fvana")
        assert response.status_code == 204
