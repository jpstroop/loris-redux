#!/usr/bin/env python

from loris.handlers import route_patterns
from loris.handlers.identifier_handler import IdentifierHandler
from loris.handlers.image_handler import ImageHandler
from loris.handlers.info_handler import InfoHandler
from tornado.ioloop import IOLoop
from tornado.web import Application
import sys

class App(object):

    # From http://www.tornadoweb.org/en/stable/guide/structure.html#the-application-object
    # "... If a dictionary is passed as the third element of the URLSpec,
    # it supplies the initialization arguments which will be passed to
    # RequestHandler.initialize. Finally, the URLSpec may have a name, which
    # will allow it to be used with RequestHandler.reverse_url."
    route_list = (
        (route_patterns.info_route_pattern(), InfoHandler),
        (route_patterns.image_route_pattern(), ImageHandler),
        (route_patterns.identifier_route_pattern(), IdentifierHandler)
    )

    @staticmethod
    def _run_debug():
        debug = False
        try:
            debug = sys.argv[1] == 'debug'
            print('Running in debug mode')
        except IndexError:
            pass
        return debug

    @staticmethod
    def create():
        debug = App._run_debug()
        # See http://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings
        return Application(App.route_list, debug=debug)

if __name__ == "__main__":
    # load configs here and pass to create_app?
    app = App.create()
    app.listen(8888)
    IOLoop.current().start()
