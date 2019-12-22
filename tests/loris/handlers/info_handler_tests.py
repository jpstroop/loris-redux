from loris.constants import HEADER_ACCEPT
from loris.constants import HEADER_ACCESS_CONTROL_HEADER_ALLOWS
from loris.constants import HEADER_ACCESS_CONTROL_ALLOW_METHODS
from loris.constants import HEADER_ACCESS_CONTROL_ALLOW_ORIGIN
from loris.constants import HEADER_ACCESS_CONTROL_MAX_AGE
from loris.constants import HEADER_ALLOW
from loris.constants import HEADER_CONNECTION
from loris.constants import HEADER_CONTENT_TYPE
from loris.constants import HEADER_KEEP_ALIVE
from loris.constants import HEADER_VARY
from loris.requests.info_request import InfoRequest
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
        assert response.headers["Content-Type"] == 'application/json'
        assert body["error"] == "ResolverException"
        description = "Could not resolve identifier: nothing.jp2"
        assert body["description"] == description

    def test_info_headers(self):
        response = self.get("/loris:sample.jp2/info.json")
        assert "Etag" in response.headers
        assert response.headers["Allow"] == "GET"
        assert response.headers["Content-Type"] == 'application/ld+json;profile="http://iiif.io/api/image/3/context.json"'
        assert "Content-Length" in response.headers

    def test_json_not_ld_request(self):
        headers = {'Accept': 'application/json'}
        response = self.get("/loris:sample.jp2/info.json", headers=headers)
        assert response.headers["Content-Type"] == "application/json"

    def test_request_without_jsonld_enabled_returns_json(self):
        InfoRequest.compliance.http.features = ()
        headers = {'Accept': 'application/ld+json'}
        response = self.get("/loris:sample.jp2/info.json", headers=headers)
        assert response.headers["Content-Type"] == "application/json"

    def test_profile_link_header(self):
        response = self.get("/loris:sample.jp2/info.json")
        expected = '<http://iiif.io/api/image/3/level2.json>;rel="profile"'
        assert response.headers["Link"] == expected

    def test_profile_link_header_can_be_disabled(self):
        InfoRequest.compliance.http.features = ()
        response = self.get("/loris:sample.jp2/info.json")
        assert "Link" not in response.headers

    def test_acao_header_default(self):
        response = self.get("/loris:sample.jp2/info.json")
        assert response.headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN] == "*"

    def test_options_preflight(self):
        response = self.options("/loris:sample.jp2/info.json")
        assert response.headers[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN] == "*"

    def test_preflight_headers(self):
        response = self.options("/loris:sample.jp2/info.json")
        excluded_headers = (HEADER_ALLOW, HEADER_CONTENT_TYPE)
        included_headers = (
            HEADER_ACCESS_CONTROL_HEADER_ALLOWS,
            HEADER_ACCESS_CONTROL_ALLOW_METHODS,
            HEADER_ACCESS_CONTROL_ALLOW_ORIGIN,
            HEADER_ACCESS_CONTROL_MAX_AGE,
            HEADER_CONNECTION,
            HEADER_KEEP_ALIVE,
            HEADER_VARY
        )
        assert all([h in response.headers for h in included_headers])
        assert all([h not in response.headers for h in excluded_headers])
