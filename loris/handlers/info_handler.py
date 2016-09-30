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
        body = json.dumps( { '@id' : identifier } ).encode('utf8')
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
