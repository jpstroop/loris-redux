from loris.requests.info_request import InfoRequest
from logging import getLogger
import cherrypy
import json
logger = getLogger('loris')

class InfoHandler(object):
    exposed = True

    def GET(self, identifier):
        # how to set a header:
        cherrypy.response.headers['Content-Type'] = 'application/json'
        # how to send JSON
        body = json.dumps( { 'you' : 'win!' } ).encode('utf8')
        # how to get the method of the request:
        # cherrypy.log(cherrypy.request.method)
        #
        # How to get the server url:
        # cherrypy.log(cherrypy.url())
        #
        # how to get the request headers:
        # for k in cherrypy.request.headers.keys():
        #     cherrypy.log('{0}: {1}'.format(k, cherrypy.request.headers[k]))
        return body

# Old Tornado handler:
# class InfoHandler(RequestHandler):
#     # See http://www.tornadoweb.org/en/stable/web.html#entry-points
#     # and http://www.tornadoweb.org/en/stable/guide/structure.html#overriding-requesthandler-methods
#
#     def get(self, identifier):
#         # Make an InfoRequest, check the etag, and then get if necessary
#         # check the etag
#         # if the etag doesn't make, call #fulfill
#         self.write('Compliance URI: ' + InfoRequest.compliance.uri)
