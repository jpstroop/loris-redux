from loris.constants import JSON_CONTENT_TYPE
from loris.constants import JSONLD_CONTENT_TYPE
from loris.constants import JSONLD_MEDIA_TYPE
from loris.exceptions import LorisException
from loris.handlers.profile_header_mixin import ProfileHeaderMixin
from loris.requests.info_request import InfoRequest
import cherrypy
import json

class InfoHandler(ProfileHeaderMixin):

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
            if self._profile_header_enabled:
                cherrypy.response.headers['Link'] = self._profile_header
            accept = cherrypy.request.headers.get('accept')
            acceptable = (JSONLD_CONTENT_TYPE, None, '*/*')
            if accept in acceptable and self._jsonld_enabled:
                cherrypy.response.headers['content-type'] = JSONLD_CONTENT_TYPE
            else:
                cherrypy.response.headers['content-type'] = JSON_CONTENT_TYPE
            cherrypy.response.headers['etag'] = info_request.etag
            return str(info_request).encode('utf8')

    @property
    def _jsonld_enabled(self):
        return JSONLD_MEDIA_TYPE in InfoRequest.compliance.http.features

    # TODO: These can be moved into a mixin. Not sure about _conditional_response
    def _etag_match(self, info_request):
        return cherrypy.request.headers.get('if-none-match') == info_request.etag

    def _error_response(self, loris_exception):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.status = loris_exception.http_status_code
        return str(loris_exception).encode('utf8')
