from loris.handlers import route_patterns
from loris.handlers.identifier_handler import IdentifierHandler
from loris.handlers.image_handler import ImageHandler
from loris.handlers.info_handler import InfoHandler
from loris.helpers.compliance import Compliance
from os import path
from tornado.web import Application
import json
import logging
import logging.config
import sys

class App(object):

    routes = None

    @staticmethod
    def _create_route_list(compliance, base_uri, extractors):
        # From:
        # http://www.tornadoweb.org/en/stable/guide/structure.html#the-application-object
        # "... If a dictionary is passed as the third element of the URLSpec,
        # it supplies the initialization arguments which will be passed to
        # RequestHandler.initialize. Finally, the URLSpec may have a name, which
        # will allow it to be used with RequestHandler.reverse_url."
        info_init_args = {
            'compliance' : compliance,
            'base_uri' : base_uri,
            'extractors' : extractors
        }
        img_init_args = {
            'compliance' : compliance
            # probably should pass transcoders as well, just to be consistent.
        }
        id_init_args = {
            'compliance' : compliance
        }
        route_list = (
            (route_patterns.info_route_pattern(), InfoHandler, info_init_args),
            (route_patterns.image_route_pattern(), ImageHandler, img_init_args),
            (route_patterns.identifier_route_pattern(), IdentifierHandler, id_init_args)
            # TODO: we need a fallback handler (/id/random)
            # TODO: favicon
        )
        return route_list

    @staticmethod
    def _run_debug():  # pragma: no cover
        debug = False
        try:
            debug = sys.argv[1] == 'debug'
            print('Running in debug mode')
        except IndexError:
            pass
        return debug

    @staticmethod
    def _init_compliance(cfg):
        compliance = Compliance(cfg)
        msg = 'Compliance is level {}'.format(compliance.server_compliance)
        logger.info(msg)
        return compliance

    @staticmethod
    def _init_base_uri(cfg):
        return cfg.get('base_uri')

    @staticmethod
    def _init_extractors():
        lookup = {}
        # lookup['jp2'] = JP2extractor()
        # lookup['jpg'] = JPEGextractor()
        # etc.
        return lookup

    def _configure(debug=False):  # pragma: no cover
        cfg_dict = App._load_config_file(debug=debug)
        App._configure_logging(cfg_dict['logging'])
        compliance = App._init_compliance(cfg_dict['features'])
        base_uri = App._init_base_uri(cfg_dict['application'])
        extractors = App._init_extractors()
        App.routes = App._create_route_list(compliance, base_uri, extractors)

    @staticmethod
    def _load_config_file(debug=False):  # pragma: no cover
        cfg_file_path = App._find_config_file(debug=debug)
        cfg_dict = None
        with open(cfg_file_path) as cfg_file:
            cfg_dict = json.load(cfg_file)
        return cfg_dict

    @staticmethod
    def _find_config_file(debug=False): # pragma: no cover
        if debug:
            project_dir = path.dirname(path.dirname(path.realpath(__file__)))
            return path.join(project_dir, 'config.json')
        else:
            pass
            # TODO: Figure out where we want to look for config. Seems like
            # the app owner's home, then /etc/whatev, and then somewhere
            # packaged with the app.

    @staticmethod
    def _configure_logging(cfg_dict):  # pragma: no cover
        global logger
        logging.config.dictConfig(cfg_dict)
        logger = logging.getLogger('loris')
        logger.debug('Logging configured')

    @staticmethod
    def create():
        debug = App._run_debug()
        App._configure(debug=debug)
        # See http://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings
        return Application(App.routes, debug=debug)
