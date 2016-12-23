from loris.constants import MEDIA_TYPE_MAPPING
from loris.exceptions import LorisException
from loris.requests.image_request import ImageRequest

from logging import getLogger
import cherrypy

logger = getLogger('loris')

class ImageHandler(object):
    exposed = True
    def GET(self, identifier, iiif_params):
        cherrypy.response.headers['Allow'] = 'GET'
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
            canoncial_uri = '/{0}/{1}'.format(identifier, image_request.canonical)
            cherrypy.response.headers['Location'] = canoncial_uri
            cherrypy.response.status = 303
            return None
        else:
            transcoder = ImageRequest.transcoders[image_request.file_format]
            stream = transcoder.execute(image_request)
            media_type = MEDIA_TYPE_MAPPING[image_request.format]
            cherrypy.response.headers['content-type'] = media_type
            cherrypy.response.headers['etag'] = image_request.etag
            return stream.getvalue()

    def _etag_match(self, image_request):
        return cherrypy.request.headers.get('if-none-match') == image_request.etag

    def _error_response(self, loris_exception):
        cherrypy.response.headers['Content-Type'] = 'application/json'
        cherrypy.response.status = loris_exception.http_status_code
        return str(loris_exception).encode('utf8')

        # from PIL import Image
        # from io import BytesIO
        # sample_img = '/home/jstroop/me/05509.jpg'
        # im = Image.open(sample_img)
        # stream = BytesIO()
        # im.save(stream, format='jpeg')
        # cherrypy.response.headers['content-type'] = 'image/jpeg'
        # return stream.getvalue()
