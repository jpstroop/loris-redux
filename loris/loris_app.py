from loris.compliance import Compliance
from loris.dispatcher_mixin import DispatcherMixin
from loris.helpers.safe_lru_dict import SafeLruDict
from loris.info.jp2_extractor import Jp2Extractor
from loris.info.pillow_extractor import PillowExtractor
from loris.requests.iiif_request import IIIFRequest
from loris.resolvers import Resolvers

from os import path
from pkg_resources import resource_filename

import cherrypy
import json
import logging
import logging.config

cherrypy_app_conf = {
    '/': {
        'tools.trailing_slash.on': False,  # this should _always_ be False
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on': False
    },
    '/favicon.ico': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': resource_filename('loris', 'www/favicon.ico'),
        'tools.response_headers.on': True,
        'tools.response_headers.headers': [
            ('cache-control', 'max-age={0}, public'.format(60*60*24*365)),
            ('allow', 'GET')
        ]
    }
}

class LorisApp(DispatcherMixin):

    def __init__(self):
        super().__init__()
        cfg_dict = self._load_config_files()
        self._configure_logging(cfg_dict['logging'])

        # This is basically a cheat to keep us from having to pass so much
        # static stuff around.
        compliance = self._init_compliance(cfg_dict['iiif_features'])
        app_configs = self._normalize_app_configs(cfg_dict['application'])
        IIIFRequest.app_configs = app_configs
        IIIFRequest.compliance = compliance
        IIIFRequest.extractors = self._init_extractors(compliance, app_configs)
        IIIFRequest.info_cache = SafeLruDict(size=400)
        IIIFRequest.resolvers = self._init_resolvers(cfg_dict['resolvers'])

    @property
    def _package_dir(self): # pragma: no cover
        # Not part of CherryPy, but needed here and in LorisApp
        return path.dirname(path.realpath(__file__))

    def _normalize_app_configs(self, app_configs):
        if app_configs['server_uri'] is not None:
            if app_configs['server_uri'].endswith('/'):
                app_configs['server_uri'] = app_configs['server_uri'][:-1]
        return app_configs

    def _load_config_files(self):
        # Should probably have coverage for this. Mocks?
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
        paths.append(path.join(self._package_dir, 'config.json'))
        paths.append('/etc/loris/config.json')
        paths.append(path.expanduser('~/.loris/config.json'))
        return paths

    def _configure_logging(self, cfg_dict):  # pragma: no cover
        global logger
        logging.config.dictConfig(cfg_dict)
        logger = logging.getLogger('loris')
        logger.debug('Logging configured')

    def _init_compliance(self, cfg_dict): # pragma: no cover
        compliance = Compliance(cfg_dict)
        msg = 'Compliance is level {}'.format(int(compliance))
        logger.info(msg)
        return compliance

    def _init_extractors(self, compliance, app_configs): # pragma: no cover
        pillow_extractor = PillowExtractor(compliance, app_configs)
        jp2_extractor = Jp2Extractor(compliance, app_configs)
        return {
            'jpg' : pillow_extractor,
            'png' : pillow_extractor,
            'tif' : pillow_extractor,
            'jp2' : jp2_extractor
        }

    def _init_resolvers(self, resolver_list, include_example=True): # pragma: no cover
        resolvers = Resolvers(resolver_list)
        # add a resolver that resolves to the root of the package for viewing
        # sample files
        if include_example:
            description = '''\
This is a sample resolver to test that the server is working. Using \
`loris:sample.jp2` as an identifier should return a test image.\
'''
            cfg = { 'root' : self._package_dir, 'description' : description }
            klass = 'loris.resolvers.file_system_resolver.FileSystemResolver'
            resolvers.add_resolver(klass, 'loris', cfg)
        return resolvers
