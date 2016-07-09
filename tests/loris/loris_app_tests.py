from loris.loris_app import LorisApp
from loris.handlers.info_handler import InfoHandler
from loris.handlers.identifier_handler import IdentifierHandler
from loris.handlers.image_handler import ImageHandler
from loris.compliance import Compliance
import re

class FakeRouter(object):

    def route(self, path):
        app = LorisApp(debug=True)
        for route in app.routes:
            if re.match(route[0], path):
                return route[1]


class TestRouting(object):

    router = FakeRouter()

    def test_info_with_escaped_slash_route(self):
        assert TestRouting.router.route('/foo%2fbar/info.json') == InfoHandler

    def test_info_dot_json_required(self):
        assert TestRouting.router.route('/foo/info') != InfoHandler

    def test_fallback_to_identifer(self):
        assert TestRouting.router.route('/someid') == IdentifierHandler

    def test_fallback_to_identifer_with_trailing_slash(self):
        assert TestRouting.router.route('/someid/') == IdentifierHandler

    def test_fallback_to_identifer_with_escaped_slashes(self):
        handler = TestRouting.router.route('/some%2frando%2fid')
        assert handler == IdentifierHandler

    def test_full_full_0_default_jpg(self):
        path = '/foo%2Fbar/full/full/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_square_full_0_default_jpg(self):
        path = '/foo%2Fbar/square/full/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_px_full_0_default_jpg(self):
        path = '/foo%2Fbar/300,4,25,5000/full/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_pct_full_0_default_jpg(self):
        path = '/foo%2Fbar/30,44,25,50/full/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_pct_decimal_full_0_default_jpg(self):
        path = '/foo%2Fbar/pct:30.2,44,25,50.4/full/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_width_0_default_jpg(self):
        path = '/foo%2Fbar/full/300,/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_height_0_default_jpg(self):
        path = '/foo%2Fbar/full/,300/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_wh_0_default_jpg(self):
        path = '/foo%2Fbar/full/200,300/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_bang_wh_0_default_jpg(self):
        path = '/foo%2Fbar/full/!200,300/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_pct_0_default_jpg(self):
        path = '/foo%2Fbar/full/pct:70/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_pct_decimal_0_default_jpg(self):
        path = '/foo%2Fbar/full/pct:70.45/0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_90_default_jpg(self):
        path = '/foo%2Fbar/full/full/90/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_270_default_jpg(self):
        path = '/foo%2Fbar/full/full/270/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_decimal_default_jpg(self):
        path = '/foo%2Fbar/full/full/44.7/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_bang_0_default_jpg(self):
        path = '/foo%2Fbar/full/full/!0/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_bang_decimal_default_jpg(self):
        path = '/foo%2Fbar/full/full/!128.6/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_bang_int_default_jpg(self):
        path = '/foo%2Fbar/full/full/!90/default.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_0_color_jpg(self):
        path = '/foo%2Fbar/full/full/0/color.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_0_gray_jpg(self):
        path = '/foo%2Fbar/full/full/0/gray.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_0_bitonal_jpg(self):
        path = '/foo%2Fbar/full/full/0/bitonal.jpg'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_0_default_png(self):
        path = '/foo%2Fbar/full/full/0/default.png'
        assert TestRouting.router.route(path) == ImageHandler

    def test_full_full_0_default_webp(self):
        path = '/foo%2Fbar/full/full/0/default.webp'
        assert TestRouting.router.route(path) == ImageHandler
