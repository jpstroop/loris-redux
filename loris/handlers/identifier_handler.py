from tornado.web import RequestHandler

class IdentifierHandler(RequestHandler):
    # Request properties documented here:
    # http://tornadokevinlee.readthedocs.io/en/latest/httputil.html#tornado.httputil.HTTPServerRequest
    def get(self, identifier):
        self.write('IdentifierHandler: ' + repr(self.request.uri))
