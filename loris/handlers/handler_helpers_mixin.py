from loris.constants import PROFILE_LINK_HEADER
from loris.requests.iiif_request import IIIFRequest
import cherrypy

class HandlerHelpersMixin(object):

    @property
    def _profile_header_enabled(self):
        return PROFILE_LINK_HEADER in IIIFRequest.compliance.http.features

    @property
    def _profile_header(self):
        return f'<{IIIFRequest.compliance.uri}>;rel="profile"'

    def _etag_match(self, request):
        return cherrypy.request.headers.get('if-none-match') == request.etag

    def _error_response(self, loris_exception):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.status = loris_exception.http_status_code
        return str(loris_exception).encode('utf8')
