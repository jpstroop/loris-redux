from logging import getLogger
from loris.constants import ACCEPT_HEADER
from loris.constants import ACCESS_CONTROL_ALLOW_HEADERS_HEADER
from loris.constants import ACCESS_CONTROL_ALLOW_METHODS_HEADER
from loris.constants import ACCESS_CONTROL_ALLOW_ORIGIN_HEADER
from loris.constants import ACCESS_CONTROL_MAX_AGE_HEADER
from loris.constants import ALLOW_HEADER
from loris.constants import CONNECTION_HEADER
from loris.constants import CONTENT_TYPE_HEADER
from loris.constants import KEEP_ALIVE_HEADER
from loris.constants import VARY_HEADER
from loris.requests.iiif_request import IIIFRequest
import cherrypy

logger = getLogger('loris')

acao = ACCESS_CONTROL_ALLOW_ORIGIN_HEADER
acam = ACCESS_CONTROL_ALLOW_METHODS_HEADER
acah = ACCESS_CONTROL_ALLOW_HEADERS_HEADER
acma = ACCESS_CONTROL_MAX_AGE_HEADER
ka = KEEP_ALIVE_HEADER
va = VARY_HEADER

class CORSMixin(object):

    def OPTIONS(self, identifier=None, iiif_params=None):
        cherrypy.response.status = 204
        del cherrypy.response.headers[ALLOW_HEADER]
        del cherrypy.response.headers[CONTENT_TYPE_HEADER]
        if self.acao_config:
            cherrypy.response.headers[acah] = "Accept, If-None-Match"
            cherrypy.response.headers[acam] = "GET, OPTIONS"
            cherrypy.response.headers[acao] = self.acao_config
            cherrypy.response.headers[acma] = self.acma_config
            cherrypy.response.headers[CONNECTION_HEADER] = "Keep-Alive"
            cherrypy.response.headers[ka] = self.keep_alive_config
            cherrypy.response.headers[va] = "Origin"
        return None

    @property
    def acao_config(self):
        return IIIFRequest.app_configs[ACCESS_CONTROL_ALLOW_ORIGIN_HEADER]

    @property
    def acma_config(self):
        return IIIFRequest.app_configs[ACCESS_CONTROL_MAX_AGE_HEADER]

    @property
    def keep_alive_config(self):
        t = IIIFRequest.app_configs['cors_keep_alive_timeout']
        m = IIIFRequest.app_configs['cors_keep_alive_max']
        return f'timeout={t}, max={m}'


    def _set_acao(self):
        # This is used by subclasses, not here
        if self.acao_config:
            cherrypy.response.headers[acao] = self.acao_config
