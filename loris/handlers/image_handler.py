from logging import getLogger
from tornado.web import RequestHandler
from loris.requests.image_request import ImageRequest

logger = getLogger('loris')

class ImageHandler(RequestHandler):

    def initialize(self, compliance, info_cache, extractors, app_configs):  # pylint:disable=arguments-differ
        self.compliance = compliance

    def get(self, identifier, path_params):
        # file_path, fmt = (None, None) # TODO
        # info = info_cache['identifier']# TODO: use extractor if KeyError
        # TODO: handle loris's errors
        # image_request = ImageRequest(file_path, path_params, self.compliance, info)
        # then pass the image_request to the appropriate transcoder
        # use compliance.http.features to help w/ the response 

        logger.debug(identifier)
        logger.debug(path_params)
        self.write('Identifier: ' + identifier)
        self.write('Path: ' + path_params)
