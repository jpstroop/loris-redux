from tests.loris.handlers.base_handler_test import BaseHandlerTest

class TestFaviconHandler(BaseHandlerTest):
    # See http://docs.cherrypy.org/en/latest/advanced.html#testing-your-application
    def test_favicon(self):
        response = self.get("/favicon.ico")
        assert response.status_code == 200
        assert response.headers["Allow"] == "GET"
        assert response.headers["Content-Type"] == "image/x-icon"
        assert response.headers["Cache-Control"] == "max-age=31536000, public"
        assert response.headers["Content-Length"] == "156176"
