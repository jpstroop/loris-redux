from tests.loris.handlers.base_handler_test import BaseHandlerTest


class TestResolversHandler(BaseHandlerTest):
    def test_resolvers_redirects(self):
        with self.app_server():
            response = self.get("/resolvers", allow_redirects=False)
            assert response.status_code == 303
            assert response.headers["Location"] == "/resolvers.json"

    def test_resolvers_json_includes_sample_resolver(self):
        with self.app_server():
            response = self.get("/resolvers.json")
            assert response.status_code == 200
            assert response.headers["Content-type"] == "application/json"
            assert any([entry["prefix"] == "loris" for entry in response.json()])
