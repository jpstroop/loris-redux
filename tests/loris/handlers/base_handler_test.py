from requests import get
from unittest import TestCase

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
