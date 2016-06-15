from tornado.web import RequestHandler
from loris.helpers.classproperty import classproperty
from logging import getLogger

logger = getLogger('loris')

class InfoHandler(RequestHandler):
    # See http://www.tornadoweb.org/en/stable/web.html#entry-points
    # and http://www.tornadoweb.org/en/stable/guide/structure.html#overriding-requesthandler-methods
    def initialize(self, compliance, base_uri, extractors):
        self.compliance = compliance
        self.compliance = base_uri
        self.extractors = extractors


    # @classproperty
    # def compliance(compliance):
    #     try:
    #         return InfoHandler._static_thing
    #     except AttributeError:
    #         InfoHandler._static_thing = 'foobar'
    #         print("static thing initialized")
    #         return InfoHandler._static_thing

    def get(self, identifier):
        self.write('InfoHandler: ' + identifier)
        self.write('Compliance URI: ' + self.compliance.compliance_uri)
