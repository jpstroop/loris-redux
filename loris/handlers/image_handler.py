from logging import getLogger
from tornado.web import RequestHandler
from loris.requests.image_request import ImageRequest

logger = getLogger('loris')

# TODO: need the resolver(s)
# TODO: superclass that can call the resolver get info

class ImageHandler(RequestHandler):

    # def initialize(self, compliance, info_cache, extractors, app_configs):  # pylint:disable=arguments-differ
    #     self.compliance = compliance

    def get(self, identifier, path_params):
        # file_path, fmt, last_mod = resolver.resolve(identifier) # TODO
        # info = info_cache['file_path']# TODO: use extractor if KeyError
        # TODO: handle loris's errors
        # image_request = ImageRequest(file_path, path_params, self.compliance, info)
        # then pass the image_request to the appropriate transcoder
        # use compliance.http.features to help w/ the response
        
        # Make an InfoRequest, check the etag, and then get if necessary
        # check the etag
        # if the etag doesn't make, call #fulfill

        logger.debug(identifier)
        logger.debug(path_params)
        self.write('Identifier: ' + identifier)
        self.write('Path: ' + path_params)
