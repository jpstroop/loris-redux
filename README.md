# Loris 3

__WIP!__

A rewrite of loris using [Tornado](http://www.tornadoweb.org/en/stable/).

## Goals
 * Full Image API 2.1 support, including all optional features
 * Work with front-end caches (Varnish, Squid)
 * Abstract APIs for Parameters, Transcoders, Resolvers, Authorization, and Authentication (implementations for the latter four are given in a config file)
 * Install w/ pip
 * No WSGI!
 * http or https support
 * Option to pre-bake tiles (supply a script)
