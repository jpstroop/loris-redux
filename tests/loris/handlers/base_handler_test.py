from loris.loris_app import LorisApp
from loris.loris_app import cherrypy_app_conf

from cherrypy.test import helper
import cherrypy

# This isn't a test; it just takes care of setting up a server for hendler tests

class BaseHandlerTest(helper.CPWebCase):
    # See https://docs.cherrypy.org/en/latest/advanced.html#testing-your-application
    helper.CPWebCase.interactive = False
    helper.CPWebCase.do_gc_test = True
    def setup_server():
        cherrypy.tree.mount(LorisApp(), '/', config=cherrypy_app_conf)
    setup_server = staticmethod(setup_server)
