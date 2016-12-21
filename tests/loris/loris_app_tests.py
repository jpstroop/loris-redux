from loris.loris_app import LorisApp
from loris.loris_app import cherrypy_app_conf

from cherrypy.test import helper
from json import loads

import cherrypy

# End-to-end integration tests intended to tes handlers. If these are failing
# chances are the problem is not with LorisApp unless _maybe_ it has to do
# with headers.

class TestLorisApp(helper.CPWebCase):
    # See http://docs.cherrypy.org/en/latest/advanced.html#testing-your-application
    def setup_server():
        cherrypy.tree.mount(LorisApp(), '/', config=cherrypy_app_conf)
    setup_server = staticmethod(setup_server)

    def test_resolvers_redirects(self):
        self.getPage('/resolvers')
        self.assertStatus(303)
        self.assertHeader('Location', '/resolvers.json')

    def test_resolvers_json_includes_sample_resolver(self):
        status, headers, body = self.getPage('/resolvers.json')
        self.assertStatus(200)
        self.assertHeader('Content-type', 'application/json')
        resolver_list = loads(body.decode('utf-8'))
        assert any([entry['prefix'] == 'loris' for entry in resolver_list])

    def test_base_id_redirects(self):
        self.getPage('/nir%2fvana')
        self.assertStatus(303)
        self.assertHeader('Location', '/nir%2Fvana/info.json')

    def test_info_returns200(self):
        self.getPage('/loris:sample.jp2/info.json')
        self.assertStatus(200)

    def test_info_value(self):
        # not exhausive, just enough to know it's not something else entirely
        status, headers, body = self.getPage('/loris:sample.jp2/info.json')
        info_dict = loads(body.decode('utf-8'))
        assert info_dict['width'] == 6000
        assert info_dict['protocol'] == 'http://iiif.io/api/image'

    def test_info_exception(self):
        status, headers, body = self.getPage('/loris:nothing.jp2/info.json')
        body = loads(body.decode('utf-8'))
        self.assertStatus(404)
        self.assertHeader('Content-Type', 'application/json')
        assert body['error'] == 'ResolverException'
        assert body['description'] == 'Could not resolve identifier: nothing.jp2'

    def test_info_headers(self):
        status, headers, body = self.getPage('/loris:sample.jp2/info.json')
        headers = dict(headers)
        assert 'Etag' in headers
        self.assertHeader('Allow', 'GET')
        self.assertHeader('Content-Type', 'application/json')
        self.assertHeader('Content-Length', '760') # careful this could change

    def test_favicon(self):
        status, headers, body = self.getPage('/favicon.ico')
        self.assertStatus(200)
        self.assertHeader('Allow', 'GET')
        self.assertHeader('Content-Type', 'image/x-icon')
        self.assertHeader('Cache-Control', 'max-age=31536000, public')
        self.assertHeader('Content-Length', 156176)

    # temporary. Just makes sure we don't break rounting
    def test_image_returns200(self):
        self.getPage('/nir%2fvana/full/full/0/default.jpg')
        self.assertStatus(200)
