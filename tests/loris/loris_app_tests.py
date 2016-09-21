# from loris.compliance import Compliance
# from loris.handlers.identifier_handler import IdentifierHandler
# from loris.handlers.image_handler import ImageHandler
# from loris.handlers.info_handler import InfoHandler
from loris.loris_app import LorisApp
from cherrypy.test import helper
import cherrypy


class TestLorisApp(helper.CPWebCase):
    # See http://docs.cherrypy.org/en/latest/advanced.html#testing-your-application
    def setup_server():
        #TODO: this is also in run.py right now...
        app_conf = {
            '/': {
                'tools.trailing_slash.on': False,  # this should _always_ be False
                'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            }
        }
        cherrypy.tree.mount(LorisApp(), '/', config=app_conf)
    setup_server = staticmethod(setup_server)

    def test_base_id_redirects(self):
        self.getPage('/nir%2fvana')
        self.assertStatus(303)
        self.assertHeader('Location', '/nir%2Fvana/info.json')

    def test_info_returns200(self):
        self.getPage('/nir%2fvana/info.json')
        self.assertStatus(200)

    def test_image_returns200(self):
        self.getPage('/nir%2fvana/full/full/0/default.jpg')
        self.assertStatus(200)
