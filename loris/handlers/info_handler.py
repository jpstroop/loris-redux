from loris.requests.info_request import InfoRequest

from logging import getLogger
from tornado.web import RequestHandler

logger = getLogger('loris')

class InfoHandler(RequestHandler):
    # See http://www.tornadoweb.org/en/stable/web.html#entry-points
    # and http://www.tornadoweb.org/en/stable/guide/structure.html#overriding-requesthandler-methods

    def get(self, identifier):
        # Make an InfoRequest, check the etag, and then get if necessary
        # check the etag
        # if the etag doesn't make, call #fulfill
        self.write('Compliance URI: ' + InfoRequest.compliance.uri)
