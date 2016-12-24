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

    def test_favicon(self):
        status, headers, body = self.getPage('/favicon.ico')
        self.assertStatus(200)
        self.assertHeader('Allow', 'GET')
        self.assertHeader('Content-Type', 'image/x-icon')
        self.assertHeader('Cache-Control', 'max-age=31536000, public')
        self.assertHeader('Content-Length', 156176)
