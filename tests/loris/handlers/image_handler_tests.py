from loris.constants import HEADER_ACCEPT
from loris.constants import HEADER_ACCESS_CONTROL_ALLOW_METHODS
from loris.constants import HEADER_ACCESS_CONTROL_ALLOW_ORIGIN
from loris.constants import HEADER_ACCESS_CONTROL_HEADER_ALLOWS
from loris.constants import HEADER_ACCESS_CONTROL_MAX_AGE
from loris.constants import HEADER_ALLOW
from loris.constants import HEADER_CONNECTION
from loris.constants import HEADER_CONTENT_TYPE
from loris.constants import HEADER_KEEP_ALIVE
from loris.constants import HEADER_VARY
from loris.requests.image_request import ImageRequest
from tests.loris.handlers.base_handler_test import BaseHandlerTest
import pytest


class TestImageHandler(BaseHandlerTest):
    @pytest.mark.filterwarnings("ignore:unclosed file")
    def test_image_returns200(self):
        response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
        assert response.status_code == 200

    @pytest.mark.filterwarnings("ignore:unclosed file")
    def test_profile_link_header_included(self):
        response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
        expected = '<http://iiif.io/api/image/3/level2.json>;rel="profile"'
        assert response.headers["Link"] == expected

    @pytest.mark.filterwarnings("ignore:unclosed file")
    def test_profile_link_header_can_be_disabled(self):
        ImageRequest.compliance.http.features = ()
        response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
        assert "Link" not in response.headers

    @pytest.mark.filterwarnings("ignore:unclosed file")
    def test_image_headers(self):
        response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
        assert "Etag" in response.headers
        assert response.headers["Allow"] == "GET"
        assert response.headers["Content-Type"] == "image/jpeg"
        assert response.headers["Content-Length"] == "6015"

    def test_redirect_to_canonical(self):
        path = "/loris:sample.jp2/full/pct:5/0/default.jpg"
        response = self.get(path, allow_redirects=False)
        canonical = "/loris:sample.jp2/full/300,400/0/default.jpg"
        assert response.headers["Location"] == canonical

    @pytest.mark.filterwarnings("ignore:unclosed file")
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
        #                                                #^
        body = response.json()
        assert response.status_code == 400
        assert body["error"] == "SyntaxException"
        description = "could not convert string to float: '10,'"
        assert body["description"] == description

    def test_acao_header_default(self):
        response = self.get("/loris:sample.jp2/full/200,/0/default.jpg")
        assert response.headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN] == "*"

    def test_options_preflight(self):
        response = self.options("/loris:sample.jp2/full/200,/0/default.jpg")
        assert response.headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN] == "*"

    def test_preflight_headers(self):
        response = self.options("/loris:sample.jp2/full/200,/0/default.jpg")
        excluded_headers = (HEADER_ALLOW, HEADER_CONTENT_TYPE)
        included_headers = (
            HEADER_ACCESS_CONTROL_ALLOW_METHODS,
            HEADER_ACCESS_CONTROL_ALLOW_ORIGIN,
            HEADER_ACCESS_CONTROL_HEADER_ALLOWS,
            HEADER_ACCESS_CONTROL_MAX_AGE,
            HEADER_CONNECTION,
            HEADER_KEEP_ALIVE,
            HEADER_VARY,
        )
        assert all([h in response.headers for h in included_headers])
        assert all([h not in response.headers for h in excluded_headers])
