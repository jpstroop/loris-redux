from tornado.web import RequestHandler

class ImageHandler(RequestHandler):

    def initialize(self, compliance, info_cache, extractors, app_configs):  # pylint:disable=arguments-differ
        self.compliance = compliance

    def get(self, identifier, region, size, rotation, quality, format):
        self.write('ImageHandler: ' + repr(self.request.uri))
