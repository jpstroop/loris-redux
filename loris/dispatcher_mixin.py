from loris.handlers.identifier_handler import IdentifierHandler
from loris.handlers.image_handler import ImageHandler
from loris.handlers.info_handler import InfoHandler
from loris.handlers.resolvers_handler import ResolversHandler
from os import path
import cherrypy

# This mixin class provides the `_cp_dispatch` method that CherryPy needs to
# route requests


class DispatcherMixin(object):
    def __init__(self):
        self.identifier_handler = IdentifierHandler()
        self.image_handler = ImageHandler()
        self.info_handler = InfoHandler()
        self.resolvers_handler = ResolversHandler()

    def _cp_dispatch(self, vpath):  # pylint:disable=protected-access
        # This is the routing. CherryPy calls this method.

        # TODO: len(vpath) == 0
        # GET is info about the server
        # POST could allow placement of images on the server.

        if len(vpath) == 1:
            val = vpath.pop()
            # resolvers / resolvers.json
            if val in ("resolvers", "resolvers.json"):
                cherrypy.request.params["val"] = val
                return self.resolvers_handler
                # return self.favicon_handler
            # base URI
            else:
                cherrypy.request.params["identifier"] = val
                return self.identifier_handler

        if len(vpath) == 2:
            if vpath.pop() != "info.json":
                raise  # TODO: raise what?
            cherrypy.request.params["identifier"] = vpath.pop()
            return self.info_handler

        if len(vpath) == 5:
            cherrypy.request.params["identifier"] = vpath[0]
            cherrypy.request.params["iiif_params"] = "/".join(vpath[1:])
            vpath[:] = []
            return self.image_handler

        return vpath
