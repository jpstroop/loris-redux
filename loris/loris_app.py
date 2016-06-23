#!/usr/bin/env python

from loris.handlers import route_patterns
from loris.handlers.identifier_handler import IdentifierHandler
from loris.handlers.image_handler import ImageHandler
from loris.handlers.info_handler import InfoHandler
from loris.helpers.compliance import Compliance
from loris.helpers.safe_lru_dict import SafeLruDict
from loris.info.pillow_extractor import PillowExtractor
from os import path
from tornado.web import Application
import json
import logging
import logging.config
import sys

class LorisApp(object):

    def __init__(self, debug=False):
        # This should not be used directly, except in testing. Generally
        # one should call LorisApp.create_tornado_application(), which will
        # initialize and configure the application.
        cfg_dict = self._load_config_file(debug=debug)
        _ = self._configure_logging(cfg_dict['logging'])
        self.compliance = self._init_compliance(cfg_dict['features'])
        self.app_configs = cfg_dict['application']
        self.extractors = self._init_extractors()
        self.info_cache = SafeLruDict(size=400)
        self.routes = self._create_route_list()

    def _load_config_file(self, debug=False):  # pragma: no cover
        cfg_file_path = self._find_config_file(debug=debug)
        cfg_dict = None
        with open(cfg_file_path) as cfg_file:
            cfg_dict = json.load(cfg_file)
        return cfg_dict

    def _find_config_file(self, debug=False): # pragma: no cover
        if debug:
            package_dir = path.dirname(path.realpath(__file__))
            return path.join(package_dir, 'config.json')
        else:
            pass
            # TODO: Figure out where we want to look for config. Seems like
            # ~/.loris/config.json
            # /etc/loris/config.json, and then
            # packaged with the app.
            # Should they inherit?

    def _configure_logging(self, cfg_dict):  # pragma: no cover
        global logger
        logging.config.dictConfig(cfg_dict)
        logger = logging.getLogger('loris')
        logger.debug('Logging configured')

    def _init_compliance(self, cfg_dict):
        compliance = Compliance(cfg_dict)
        msg = 'Compliance is level {}'.format(compliance.level)
        logger.info(msg)
        return compliance

    def _init_extractors(self):
        pillow_extractor = PillowExtractor(self.compliance, self.app_configs)
        # jp2_extractor = Jp2Extractor(self.compliance)
        return {
            'jpg' : pillow_extractor,
            'png' : pillow_extractor,
            'tif' : pillow_extractor,
            # 'jp2' : jp2_extractor
        }

    def _create_route_list(self):
        # From:
        # http://www.tornadoweb.org/en/stable/guide/structure.html#the-application-object
        # "... If a dictionary is passed as the third element of the URLSpec,
        # it supplies the initialization arguments which will be passed to
        # RequestHandler.initialize. Finally, the URLSpec may have a name, which
        # will allow it to be used with RequestHandler.reverse_url."
        info_init_args = {
            'compliance' : self.compliance,
            'info_cache' : self.info_cache,
            'extractors' : self.extractors,
            'app_configs' : self.app_configs
        }
        img_init_args = {
            'compliance' : self.compliance,
            'info_cache' : self.info_cache,
            'extractors' : self.extractors,
            'app_configs' : self.app_configs
            # 'transcoders' : self.transcoders
        }
        id_init_args = {
            'compliance' : self.compliance
        }
        return (
            (route_patterns.info_route_pattern(), InfoHandler, info_init_args),
            (route_patterns.image_route_pattern(), ImageHandler, img_init_args),
            (route_patterns.identifier_route_pattern(), IdentifierHandler, id_init_args)
            # TODO: we need a fallback handler (/id/random)
            # TODO: favicon
        )

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
    def create_tornado_application():
        debug = LorisApp._run_debug()
        loris_app = LorisApp(debug=debug)
        # See http://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings
        return Application(loris_app.routes, debug=debug)
