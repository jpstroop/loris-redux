from loris.compliance import Compliance
from loris.handlers.identifier_handler import IdentifierHandler
from loris.handlers.image_handler import ImageHandler
from loris.handlers.info_handler import InfoHandler
from loris.helpers.safe_lru_dict import SafeLruDict
from loris.info.jp2_extractor import Jp2Extractor
from loris.info.pillow_extractor import PillowExtractor
from loris.requests.iiif_request import IIIFRequest

from os import path

import cherrypy
import json
import logging
import logging.config
import sys

class LorisApp(object):

    def __init__(self):
        cfg_dict = self._load_config_files()
        self._configure_logging(cfg_dict['logging'])
        self.identifier_handler = IdentifierHandler()
        self.info_handler = InfoHandler()
        self.image_handler = ImageHandler()

        # This is basically a cheat to keep us from having to pass so much
        # static stuff around.
        compliance = self._init_compliance(cfg_dict['iiif_features'])
        app_configs = self._normalize_app_configs(cfg_dict['application'])
        IIIFRequest.extractors = self._init_extractors(compliance, app_configs)
        IIIFRequest.info_cache = SafeLruDict(size=400)
        IIIFRequest.compliance = compliance
        IIIFRequest.app_configs = app_configs

    def _normalize_app_configs(self, app_configs):
        if app_configs['server_uri'] is not None:
            if app_configs['server_uri'].endswith('/'):
                app_configs['server_uri'] = app_configs['server_uri'][:-1]
        return app_configs

    def _load_config_files(self): # Should probably have coverage for this. Mocks?
        cfg_dict = {}
        for cfg_path in self._find_config_files():
            try:
                cfg_dict.update(self._load_json_file(cfg_path))
                print('Config file found at {0}'.format(cfg_path))
            except FileNotFoundError:
                print('No config file found at {0}'.format(cfg_path))
        return cfg_dict

    def _load_json_file(self, json_path): # pragma: no cover
        with open(json_path) as p:
            return json.load(p)

    def _find_config_files(self): # pragma: no cover
        # TODO: https://github.com/jpstroop/loris-redux/issues/44
        # returns paths to the config files in order of preference
        paths = []
        package_dir = path.dirname(path.realpath(__file__))
        paths.append(path.join(package_dir, 'config.json'))
        paths.append('/etc/loris/config.json')
        paths.append(path.expanduser('~/.loris/config.json'))
        return paths

    def _configure_logging(self, cfg_dict):  # pragma: no cover
        global logger
        logging.config.dictConfig(cfg_dict)
        logger = logging.getLogger('loris')
        logger.debug('Logging configured')

    def _init_compliance(self, cfg_dict):
        compliance = Compliance(cfg_dict)
        msg = 'Compliance is level {}'.format(int(compliance))
        logger.info(msg)
        return compliance

    def _init_extractors(self, compliance, app_configs):
        pillow_extractor = PillowExtractor(compliance, app_configs)
        jp2_extractor = Jp2Extractor(compliance, app_configs)
        return {
            'jpg' : pillow_extractor,
            'png' : pillow_extractor,
            'tif' : pillow_extractor,
            'jp2' : jp2_extractor
        }

    def _cp_dispatch(self, vpath):

        # TODO: len(vpath) == 0
        # GET is info about the server
        # POST could allow placement of images on the server.

        if len(vpath) == 1:
            cherrypy.request.params['identifier'] = vpath.pop()
            return self.identifier_handler

        if len(vpath) == 2:
            if vpath.pop() != 'info.json':
                raise
            cherrypy.request.params['identifier'] = vpath.pop()
            return self.info_handler

        if len(vpath) == 5:
            cherrypy.request.params['identifier'] = vpath[0]
            cherrypy.request.params['iiif_params'] = '/'.join(vpath[1:])
            vpath[:] = []
            return self.image_handler

        return vpath

    @cherrypy.expose
    def index(self):
        # TODO: link to loris.io
        return 'This is Loris.'
