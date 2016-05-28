from tornado.web import RequestHandler

class ImageHandler(RequestHandler):
    def get(self, identifier, region, size, rotation, quality, format):
        self.write('ImageHandler: ' + repr(self.request.uri))
