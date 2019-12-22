from loris.constants import ACCEPT_HEADER
from loris.constants import ACCESS_CONTROL_ALLOW_HEADERS_HEADER
from loris.constants import ACCESS_CONTROL_ALLOW_METHODS_HEADER
from loris.constants import ACCESS_CONTROL_ALLOW_ORIGIN_HEADER
from loris.constants import ACCESS_CONTROL_MAX_AGE_HEADER
from loris.constants import ALLOW_HEADER
from loris.constants import CONNECTION_HEADER
from loris.constants import CONTENT_TYPE_HEADER
from loris.constants import KEEP_ALIVE_HEADER
from loris.constants import VARY_HEADER
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
        assert response.headers[ACCESS_CONTROL_ALLOW_ORIGIN_HEADER] == "*"

    def test_options_preflight(self):
        response = self.options("/loris:sample.jp2/full/200,/0/default.jpg")
        assert response.headers[ACCESS_CONTROL_ALLOW_ORIGIN_HEADER] == "*"

    def test_preflight_headers(self):
        response = self.options("/loris:sample.jp2/full/200,/0/default.jpg")
        excluded_headers = (ALLOW_HEADER, CONTENT_TYPE_HEADER)
        included_headers = (
            ACCESS_CONTROL_ALLOW_HEADERS_HEADER,
            ACCESS_CONTROL_ALLOW_METHODS_HEADER,
            ACCESS_CONTROL_ALLOW_ORIGIN_HEADER,
            ACCESS_CONTROL_MAX_AGE_HEADER,
            CONNECTION_HEADER,
            KEEP_ALIVE_HEADER,
            VARY_HEADER
        )
        assert all([h in response.headers for h in included_headers])
        assert all([h not in response.headers for h in excluded_headers])
