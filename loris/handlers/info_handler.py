from tornado.web import RequestHandler
from loris.helpers.classproperty import classproperty
from logging import getLogger

logger = getLogger('loris')

class InfoHandler(RequestHandler):
    # See http://www.tornadoweb.org/en/stable/web.html#entry-points
    # and http://www.tornadoweb.org/en/stable/guide/structure.html#overriding-requesthandler-methods
    # Expensive static stuff as a static property
    def initialize(self, compliance):
        self.compliance = compliance

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
