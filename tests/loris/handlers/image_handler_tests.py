from tests.loris.handlers.base_handler_test import BaseHandlerTest
import pytest


class TestImageHandler(BaseHandlerTest):
    def test_image_returns200(self):
        response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
        assert response.status_code == 200

    def test_image_headers(self):
        response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
        assert "Etag" in response.headers
        assert response.headers["Allow"] == "GET"
        assert response.headers["Content-Type"] == "image/jpeg"
        assert response.headers["Content-Length"] == "5962"

    def test_redirect_to_canonical(self):
        path = "/loris:sample.jp2/full/pct:5/0/default.jpg"
        response = self.get(path, allow_redirects=False)
        canonical = "/loris:sample.jp2/full/300,/0/default.jpg"
        assert response.headers["Location"] == canonical

    @pytest.mark.filterwarnings("ignore:the imp module is deprecated")
    def test_etag_works(self):
        path = "/loris:sample.jp2/full/200,/0/default.jpg"
        response = self.get(path)
        etag = response.headers["Etag"]
        headers = {"if-none-match": etag}
        response1 = self.get(path, headers=headers)
        assert response1.status_code == 304

    def test_400_for_bad_syntax(self):
        response = self.get("/loris:sample.jp2/full/pct:10,/0/default.jpg")
        body = response.json()
        assert response.status_code == 400
        assert body["error"] == "SyntaxException"
        description = "could not convert string to float: '10,'"
        assert body["description"] == description
