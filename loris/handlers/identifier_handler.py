import cherrypy

class IdentifierHandler(object):
    exposed = True
    def GET(self, identifier):
        info_uri = '/{0}/info.json'.format(identifier)
        del cherrypy.response.headers['Content-Type']
        cherrypy.response.headers['Location'] = info_uri
        cherrypy.response.status = 303

        return None
    # index._cp_config = {'tools.trailing_slash.on' : False}

    def PURGE(self, identifier):
        # TODO: to purge any source images that have been cached locally
        return 'You purged {0}\n'.format(identifier)
