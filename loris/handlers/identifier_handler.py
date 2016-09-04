from tornado.web import RequestHandler


class IdentifierHandler(RequestHandler):

    def initialize(self, compliance): # pylint:disable=arguments-differ
        self.compliance = compliance
    # Request properties documented here:
    # http://tornadokevinlee.readthedocs.io/en/latest/httputil.html#tornado.httputil.HTTPServerRequest
    def get(self, identifier):
        self.write('IdentifierHandler: ' + repr(self.request.uri))
