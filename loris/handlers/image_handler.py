from logging import getLogger
import cherrypy

logger = getLogger('loris')

class ImageHandler(object):
    exposed = True
    def GET(self, identifier, iiif_params):
        # image_request = ImageRequest(identifier, iiif_params)
        # if etag matches:
        #   304
        # elif iiif_params != image_request.canoncial
        #   303 to '/'.join((identifier, iiif_params))
        # else
        #   look up the right transcoder using image_request.file_format:
        #   transcoder = IIIFRequest.transcoders[image_request.file_format]
        #   and:
        #   return transcoder.transcode(image_request)
        #   which should return bytes, I believe
        # All of this should be wrapped in a try that handles LorisExceptions
        # similar to the InfoHandler (can probably push the etag and error
        # handling up to a shared Mixin.)
        return 'This must be an image request. id: {0}, Params: {1}'.format(identifier, iiif_params)
