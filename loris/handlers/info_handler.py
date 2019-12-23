from logging import getLogger
from loris.constants import FEATURE_JSONLD_MEDIA_TYPE
from loris.constants import MEDIA_TYPE_JSON
from loris.constants import MEDIA_TYPE_JSONLD
from loris.exceptions import LorisException
from loris.handlers.cors_mixin import CORSMixin
from loris.handlers.handler_helpers_mixin import HandlerHelpersMixin
from loris.requests.info_request import InfoRequest
import cherrypy
import json

logger = getLogger("loris")


class InfoHandler(HandlerHelpersMixin, CORSMixin):

    exposed = True  # This is for CherryPy.

    def GET(self, identifier):
        cherrypy.response.headers["Allow"] = "GET"
        self._set_acao()
        try:
            return self._conditional_response(identifier)
        except LorisException as le:
            return self._error_response(le)

    def _conditional_response(self, identifier):
        info_request = InfoRequest(identifier)
        if self._etag_match(info_request):
            cherrypy.response.headers.pop("content-type", None)
            cherrypy.response.status = 304
            return None
        else:
            if self._profile_header_enabled:
                cherrypy.response.headers["Link"] = self._profile_header
            accept = cherrypy.request.headers.get("accept")
            acceptable = (MEDIA_TYPE_JSONLD, None, "*/*")
            if accept in acceptable and self._jsonld_enabled:
                cherrypy.response.headers["content-type"] = MEDIA_TYPE_JSONLD
            else:
                cherrypy.response.headers["content-type"] = MEDIA_TYPE_JSON
            cherrypy.response.headers["etag"] = info_request.etag
            return str(info_request).encode("utf8")

    @property
    def _jsonld_enabled(self):
        return FEATURE_JSONLD_MEDIA_TYPE in InfoRequest.compliance.http.features
