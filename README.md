# loris-redux

[![Build Status](https://travis-ci.org/jpstroop/loris-redux.svg?branch=master)](https://travis-ci.org/jpstroop/loris-redux) [![Coverage Status](https://coveralls.io/repos/github/jpstroop/loris-redux/badge.svg?branch=master)](https://coveralls.io/github/jpstroop/loris-redux?branch=master)

__WIP!__

A rewrite of loris using [Tornado](http://www.tornadoweb.org/en/stable/).

## Stuff you can do now

### Run the server in debug mode

```
$ pip install -r requirements.txt
$ loris/run.py debug
```

### Run tests

```
$ python setup.py test
```


## Goals
 * Full Image API 2.1 support, including all optional features
 * Work with front-end caches (Varnish, Squid)
 * Abstract APIs for Parameters, Transcoders, Resolvers, Authorization, and Authentication (implementations for the latter four are given in a config file)
 * Install w/ pip
 * No WSGI!
 * http or https support
 * Option to pre-bake tiles (supply a script)
 * Store and Delete source files on the server over HTTP
 * Enable and disable specific features, and dynamically determine compliance level
