from loris.constants import MEDIA_TYPE_MAPPING
from loris.exceptions import LorisException
from loris.requests.image_request import ImageRequest
from loris.handlers.cors_mixin import CORSMixin
from loris.handlers.handler_helpers_mixin import HandlerHelpersMixin
from logging import getLogger
import cherrypy

logger = getLogger('loris')

class ImageHandler(HandlerHelpersMixin, CORSMixin):

    exposed = True

    def GET(self, identifier, iiif_params):
        cherrypy.response.headers['Allow'] = 'GET'
        self._set_acao()
        del cherrypy.response.headers['Content-Type']
        try:
            return self._conditional_response(identifier, iiif_params)
        except LorisException as le:
            return self._error_response(le)

    def _conditional_response(self, identifier, iiif_params):
        image_request = ImageRequest(identifier, iiif_params)
        if self._etag_match(image_request):
            cherrypy.response.status = 304
            return None
        elif iiif_params != image_request.canonical:
            canoncial_uri = f'/{identifier}/{image_request.canonical}'
            cherrypy.response.headers['Location'] = canoncial_uri
            cherrypy.response.status = 303
            return None
        else:
            transcoder = ImageRequest.transcoders[image_request.file_format]
            stream = transcoder.execute(image_request)
            media_type = MEDIA_TYPE_MAPPING[image_request.format]
            if self._profile_header_enabled:
                cherrypy.response.headers['Link'] = self._profile_header
            cherrypy.response.headers['content-type'] = media_type
            cherrypy.response.headers['etag'] = image_request.etag
            return stream.getvalue()
