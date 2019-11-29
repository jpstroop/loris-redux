from contextlib import contextmanager
from loris.loris_app import cherrypy_app_conf
from loris.loris_app import LorisApp
from requests import get
from unittest import TestCase
import cherrypy

# This isn't a test; it just takes care of setting up a server for hendler tests

SOCKET_PORT = 5004
SOCKET_HOST = "127.0.0.1"


class BaseHandlerTest(TestCase):
    def get(self, path, **kwargs):
        """Wrapper around requests.get that allows for getting just the path of
        the server request from the server that is run by the `self.app_server`
        context manager.
        """
        if path.startswith("/"):
            path = path[1:]
        uri = f"http://{SOCKET_HOST}:{SOCKET_PORT}/{path}"
        return get(uri, **kwargs)

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

    def _configure(self):
        server_conf = {
            "server.socket_port": SOCKET_PORT,
            "server.socket_host": SOCKET_HOST,
        }
        cherrypy.config.update(server_conf)
        cherrypy.tree.mount(LorisApp(), "/", config=cherrypy_app_conf)
