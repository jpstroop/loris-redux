from tests.loris.handlers.base_handler_test import BaseHandlerTest


class TestIdentifierHandler(BaseHandlerTest):
    def test_base_id_redirects(self):
        # with self.app_server():
        response = self.get("/nir%2fvana", allow_redirects=False)
        assert response.status_code == 303
        assert response.headers["Location"] == "/nir%2Fvana/info.json"
