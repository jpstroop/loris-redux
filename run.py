#!/usr/bin/env python
from loris.loris_app import LorisApp
from loris.loris_app import cherrypy_app_conf


import cherrypy

cherrypy._cpconfig.environments['staging']['engine.autoreload.on'] = True

server_conf = {
    # take this as a command line option or value in the config file
    # 'environment': 'staging', TODO: what is the 'development' env?
    'server.socket_port': 5004,
    'server.socket_host': '127.0.0.1'
    # 'server.socket_host' : 'myserver.edu'
}



# To start the server, the app should take:
#  * Port (default 5004)
#  * hostname (default localhost?)
#  * environment (default staging)
#  * loris config file path?

# Questions:
#  * run as different user?
#  * Init script?

# Re. configuration: http://docs.cherrypy.org/en/latest/basics.html#additional-application-settings
# and http://docs.cherrypy.org/en/latest/config.html
cherrypy.config.update(server_conf)
cherrypy.quickstart(LorisApp(), config=cherrypy_app_conf)

# TODO: Environments:
# http://docs.cherrypy.org/en/3.3.0/tutorial/config.html?highlight=environments#environments

# An init script could look something like this:
# from cherrypy.process.plugins import Daemonizer
# Daemonizer(cherrypy.engine).subscribe()
# cherrypy.config.update(server_conf)
# cherrypy.tree.mount(LorisApp(), '/', config=app_conf)
# cherrypy.engine.start()
# cherrypy.engine.block()
# Useful links: http://docs.c
