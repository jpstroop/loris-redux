from tests.loris.handlers.base_handler_test import BaseHandlerTest

from json import loads


class TestInfoHandler(BaseHandlerTest):
    def test_info_returns200(self):
        self.getPage("/loris:sample.jp2/info.json")
        self.assertStatus(200)

    def test_info_value(self):
        # not exhausive, just enough to know it's not something else entirely
        status, headers, body = self.getPage("/loris:sample.jp2/info.json")
        info_dict = loads(body.decode("utf-8"))
        assert info_dict["width"] == 6000
        assert info_dict["protocol"] == "http://iiif.io/api/image"

    def test_info_exception(self):
        status, headers, body = self.getPage("/loris:nothing.jp2/info.json")
        body = loads(body.decode("utf-8"))
        self.assertStatus(404)
        self.assertHeader("Content-Type", "application/json")
        assert body["error"] == "ResolverException"
        assert (
            body["description"] == "Could not resolve identifier: nothing.jp2"
        )

    def test_info_headers(self):
        status, headers, body = self.getPage("/loris:sample.jp2/info.json")
        headers = dict(headers)
        assert "Etag" in headers
        self.assertHeader("Allow", "GET")
        self.assertHeader("Content-Type", "application/json")
        self.assertHeader("Content-Length", "760")  # careful this could change
