from tornado.web import RequestHandler
from loris.helpers.classproperty import classproperty

class InfoHandler(RequestHandler):
    # See http://www.tornadoweb.org/en/stable/web.html#entry-points
    # and http://www.tornadoweb.org/en/stable/guide/structure.html#overriding-requesthandler-methods

    # Expensive static stuff as a static property
    @classproperty
    def static_thing(cls):
        try:
            return InfoHandler._static_thing
        except AttributeError:
            InfoHandler._static_thing = 'foobar'
            print("static thing initialized")
            return InfoHandler._static_thing

    def get(self, identifier):
        self.write('InfoHandler: ' + identifier)
        print(self.static_thing)
