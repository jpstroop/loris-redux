from loris.exceptions import LorisException
from loris.requests.info_request import InfoRequest
import cherrypy
import json

class InfoHandler(object):

    exposed = True # This is for CherryPy.

    def GET(self, identifier):
        cherrypy.response.headers['Allow'] = 'GET'
        try:
            return self._conditional_response(identifier)
        except LorisException as le:
            return self._error_response(le)

    def _conditional_response(self, identifier):
        info_request = InfoRequest(identifier)
        if self._etag_match(info_request):
            cherrypy.response.headers.pop('content-type', None)
            cherrypy.response.status = 304
            return None
        else:
            cherrypy.response.headers['content-type'] = 'application/json'
            cherrypy.response.headers['etag'] = info_request.etag
            return str(info_request).encode('utf8')

    # TODO: These can be moved into a mixin. Not sure about _conditional_response
    def _etag_match(self, info_request):
        return cherrypy.request.headers.get('if-none-match') == info_request.etag

    def _error_response(self, loris_exception):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.status = loris_exception.http_status_code
        return str(loris_exception).encode('utf8')
