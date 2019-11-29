from tests.loris.handlers.base_handler_test import BaseHandlerTest


class TestInfoHandler(BaseHandlerTest):
    def test_info_returns200(self):
        response = self.get("/loris:sample.jp2/info.json")
        assert response.status_code == 200

    def test_info_value(self):
        # not exhausive, just enough to know it's not something else entirely
        response = self.get("/loris:sample.jp2/info.json")
        body = response.json()
        assert body["width"] == 6000
        assert body["protocol"] == "http://iiif.io/api/image"

    def test_info_exception(self):
        response = self.get("/loris:nothing.jp2/info.json")
        body = response.json()
        assert response.status_code == 404
        assert response.headers["Content-Type"] == "application/json"
        assert body["error"] == "ResolverException"
        description = "Could not resolve identifier: nothing.jp2"
        assert body["description"] == description

    def test_info_headers(self):
        response = self.get("/loris:sample.jp2/info.json")
        assert "Etag" in response.headers
        assert response.headers["Allow"] == "GET"
        assert response.headers["Content-Type"] == "application/json"
        # Careful, this could change:
        assert response.headers["Content-Length"] == "760"
