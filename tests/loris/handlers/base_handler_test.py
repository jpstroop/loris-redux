from contextlib import contextmanager
from loris.loris_app import cherrypy_app_conf
from loris.loris_app import LorisApp
from requests import get
from unittest import TestCase
import cherrypy

# This isn't a test; it just takes care of setting up a server for hendler tests

TEST_SERVER_BASE = "http://127.0.0.1:5004"

class BaseHandlerTest(TestCase):

    def get(self, path, **kwargs):
        if not path.startswith("/"):
            path = f"/{path}"
        uri = f"{TEST_SERVER_BASE}{path}"
        return get(uri, **kwargs)

    def _configure(self):
        server_conf = {
            "server.socket_port": 5004,
            "server.socket_host": "127.0.0.1",
        }
        cherrypy.config.update(server_conf)
        cherrypy.tree.mount(LorisApp(), "/", config=cherrypy_app_conf)

    @contextmanager
    def app_server(self):
        try:
            self._configure()
            cherrypy.engine.start()
            cherrypy.engine.wait(cherrypy.engine.states.STARTED)
            yield

        finally:
            cherrypy.engine.exit()
            cherrypy.engine.block()
