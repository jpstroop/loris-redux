# This mixing class provides the `_cp_dispatch` method that CherryPy needs to
# route requests
import cherrypy

class DispatcherMixin(object):

    def _cp_dispatch(self, vpath):  # pylint:disable=protected-access
        # This is the routing. cherrypy calls this method.

        # TODO: len(vpath) == 0
        # GET is info about the server
        # POST could allow placement of images on the server.

        if len(vpath) == 1:
            val = vpath.pop()
            # resolvers / resolvers.json
            if val in ('resolvers', 'resolvers.json'):
                cherrypy.request.params['val'] = val
                return self.resolvers_handler
            # base URI
            else:
                cherrypy.request.params['identifier'] = val
                return self.identifier_handler

        if len(vpath) == 2:
            if vpath.pop() != 'info.json':
                raise
            cherrypy.request.params['identifier'] = vpath.pop()
            return self.info_handler

        if len(vpath) == 5:
            cherrypy.request.params['identifier'] = vpath[0]
            cherrypy.request.params['iiif_params'] = '/'.join(vpath[1:])
            vpath[:] = []
            return self.image_handler

        return vpath

    @cherrypy.expose
    def index(self):
        # TODO: link to loris.io
        return 'This is Loris.'
