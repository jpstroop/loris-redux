from logging import getLogger
from loris.constants import HEADER_ACCEPT
from loris.constants import HEADER_ACCESS_CONTROL_HEADER_ALLOWS
from loris.constants import HEADER_ACCESS_CONTROL_ALLOW_METHODS
from loris.constants import HEADER_ACCESS_CONTROL_ALLOW_ORIGIN
from loris.constants import HEADER_ACCESS_CONTROL_MAX_AGE
from loris.constants import HEADER_ALLOW
from loris.constants import HEADER_CONNECTION
from loris.constants import HEADER_CONTENT_TYPE
from loris.constants import HEADER_KEEP_ALIVE
from loris.constants import HEADER_VARY
from loris.requests.iiif_request import IIIFRequest
import cherrypy

logger = getLogger('loris')

acao = HEADER_ACCESS_CONTROL_ALLOW_ORIGIN
acam = HEADER_ACCESS_CONTROL_ALLOW_METHODS
acah = HEADER_ACCESS_CONTROL_HEADER_ALLOWS
acma = HEADER_ACCESS_CONTROL_MAX_AGE
ka = HEADER_KEEP_ALIVE
va = HEADER_VARY

class CORSMixin(object):

    def OPTIONS(self, identifier=None, iiif_params=None):
        cherrypy.response.status = 204
        del cherrypy.response.headers[HEADER_ALLOW]
        del cherrypy.response.headers[HEADER_CONTENT_TYPE]
        if self.acao_config:
            cherrypy.response.headers[acah] = "Accept, If-None-Match"
            cherrypy.response.headers[acam] = "GET, OPTIONS"
            cherrypy.response.headers[acao] = self.acao_config
            cherrypy.response.headers[acma] = self.acma_config
            cherrypy.response.headers[HEADER_CONNECTION] = "Keep-Alive"
            cherrypy.response.headers[ka] = self.keep_alive_config
            cherrypy.response.headers[va] = "Origin"
        return None

    @property
    def acao_config(self):
        return IIIFRequest.app_configs[HEADER_ACCESS_CONTROL_ALLOW_ORIGIN]

    @property
    def acma_config(self):
        return IIIFRequest.app_configs[HEADER_ACCESS_CONTROL_MAX_AGE]

    @property
    def keep_alive_config(self):
        t = IIIFRequest.app_configs['cors_keep_alive_timeout']
        m = IIIFRequest.app_configs['cors_keep_alive_max']
        return f'timeout={t}, max={m}'


    def _set_acao(self):
        # This is used by subclasses, not here
        if self.acao_config:
            cherrypy.response.headers[acao] = self.acao_config
