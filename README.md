# loris-redux

[![Build Status](https://travis-ci.org/jpstroop/loris-redux.svg?branch=master)](https://travis-ci.org/jpstroop/loris-redux) [![Coverage Status](https://coveralls.io/repos/github/jpstroop/loris-redux/badge.svg?branch=master)](https://coveralls.io/github/jpstroop/loris-redux?branch=master)
[![Code Health](https://landscape.io/github/jpstroop/loris-redux/master/landscape.svg?style=flat)](https://landscape.io/github/jpstroop/loris-redux/master)
[![Dependency Status](https://gemnasium.com/badges/github.com/jpstroop/loris-redux.svg)](https://gemnasium.com/github.com/jpstroop/loris-redux)

[![License: New BSD](https://img.shields.io/badge/license-New%20BSD-blue.svg)](https://github.com/jpstroop/loris-redux/blob/master/LICENSE.txt)

[![Python 3.5](https://img.shields.io/badge/python-3.5-yellow.svg)](https://img.shields.io/badge/python-3.5-yellow.svg)

[![Ready](https://badge.waffle.io/jpstroop/loris-redux.svg?label=ready&title=Ready)](http://waffle.io/jpstroop/loris-redux)


__WIP!__

A rewrite of loris using [CherryPy](http://cherrypy.org/).

## Stuff you can do now

### Run the server in debug mode

```
$ pip install -r requirements.txt
$ python run.py
```

The `info.json` service is working. While the server is running go to `http://localhost:5004/loris:sample.jp2/info.json`.

There is also an extension service, `/resolvers.json` that lists the available resolvers. This is still WIP (see [#101](https://github.com/jpstroop/loris-redux/issues/101)), but the concept is there.

### Run tests

```
$ python setup.py test
```

## Goals
 * Full Image API 2.1 support, including all optional features
 * Work with front-end caches (Varnish, Squid)
 * Abstract APIs for Parameters, Transcoders, Resolvers, Authorization(?), and Authentication(?) (implementations for the latter four are given in a config file)
 * Install w/ pip
 * No WSGI!
 * https support
 * Store and Delete source files on the server over HTTP (eventually)
 * Enable and disable specific features, and dynamically determine compliance level
