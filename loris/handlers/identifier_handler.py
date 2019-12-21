from loris.constants import BASE_URI_REDIRECT
from loris.handlers.handler_helpers_mixin import HandlerHelpersMixin
from loris.requests.info_request import IIIFRequest
import cherrypy

class IdentifierHandler(HandlerHelpersMixin):
    exposed = True
    def GET(self, identifier):
        if BASE_URI_REDIRECT in IIIFRequest.compliance.http.features:
            info_uri = f'/{identifier}/info.json'
            del cherrypy.response.headers['Content-Type']
            cherrypy.response.headers['Location'] = info_uri
            cherrypy.response.status = 303
            return None
        else:
            if self._profile_header_enabled:
                cherrypy.response.headers['Link'] = self._profile_header
            cherrypy.response.status = 204

    # def PURGE(self, identifier):
    #     # TODO: to purge any source images that have been cached locally and return 204
    #     return f'You purged {identifier}\n'
