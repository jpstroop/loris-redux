from loris.requests.iiif_request import IIIFRequest
import cherrypy

class ResolversHandler(object):
    exposed = True

    def GET(self, val):
        if val == 'resolvers.json':
            cherrypy.response.headers['Content-Type'] = 'application/json'
            return IIIFRequest.resolvers.json
        else:
            del cherrypy.response.headers['Content-Type']
            cherrypy.response.headers['Location'] = '/resolvers.json'
            cherrypy.response.status = 303
            return None
