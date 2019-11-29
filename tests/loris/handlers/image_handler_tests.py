from json import loads
from tests.loris.handlers.base_handler_test import BaseHandlerTest

class TestImageHandler(BaseHandlerTest):

    def test_image_returns200(self):
        with self.app_server():
            response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
            assert response.status_code == 200

    def test_image_headers(self):
        with self.app_server():
            response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
            assert "Etag" in response.headers
            assert response.headers["Allow"] == "GET"
            assert response.headers["Content-Type"] == "image/jpeg"
            assert response.headers["Content-Length"] == "5962"
            # from sys import version_info
            # PYTHON_VERSION = ".".join(map(str, version_info[0:3]))
            # Some versions of python  == 5904 ??

    def test_redirect_to_canonical(self):
        with self.app_server():
            response = self.get("/loris:sample.jp2/full/pct:5/0/default.jpg", allow_redirects=False)
            assert response.headers["Location"] == "/loris:sample.jp2/full/300,/0/default.jpg"

    def test_etag_works(self):
        with self.app_server():
            path = "/loris:sample.jp2/full/200,/0/default.jpg"
            response = self.get(path)
            etag = response.headers["Etag"]
            headers = {"if-none-match": etag}
            response1 = self.get(path, headers=headers)
            assert response1.status_code == 304

    def test_400_for_bad_syntax(self):
        with self.app_server():
            response = self.get("/loris:sample.jp2/full/pct:10,/0/default.jpg")
            body = response.json()
            assert response.status_code == 400
            assert body["error"] == "SyntaxException"
            assert body["description"] == "could not convert string to float: '10,'"
