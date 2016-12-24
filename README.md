# loris-redux

[![Build Status](https://travis-ci.org/jpstroop/loris-redux.svg?branch=master)](https://travis-ci.org/jpstroop/loris-redux) [![Coverage Status](https://coveralls.io/repos/github/jpstroop/loris-redux/badge.svg?branch=master)](https://coveralls.io/github/jpstroop/loris-redux?branch=master) [![Code Health](https://landscape.io/github/jpstroop/loris-redux/master/landscape.svg?style=flat)](https://landscape.io/github/jpstroop/loris-redux/master) [![Dependency Status](https://gemnasium.com/badges/github.com/jpstroop/loris-redux.svg)](https://gemnasium.com/github.com/jpstroop/loris-redux)

[![License: New BSD](https://img.shields.io/badge/license-New%20BSD-blue.svg)](https://github.com/jpstroop/loris-redux/blob/master/LICENSE.txt)

[![Python 3.5](https://img.shields.io/badge/python-3.5-yellow.svg)](https://img.shields.io/badge/python-3.5-yellow.svg)
[![Python 3.6](https://img.shields.io/badge/python-3.6-yellow.svg)](https://img.shields.io/badge/python-3.6-yellow.svg)

[![Ready](https://badge.waffle.io/jpstroop/loris-redux.svg?label=ready&title=Ready)](http://waffle.io/jpstroop/loris-redux)


__WIP!__

A rewrite of loris using [CherryPy](http://cherrypy.org/) and Python `>=` 3.5.

## Stuff you can do now

### Run the server in debug mode

```
$ pip install -r requirements.txt
$ python run.py
```

 * Info: `http://localhost:5004/loris:sample.jp2/info.json`
 * Pixels: `http://localhost:5004/loris:sample.jp2/full/800,/0/default.jpg`

There is also an extension service, `/resolvers.json` that lists the available resolvers. This is still WIP (see [#101](https://github.com/jpstroop/loris-redux/issues/101)), but the concept is there.

### Run tests

```bash
$ python setup.py test
```

If you want to see logging output while running the tests, run them with pytest:

```bash
$ py.test -s <optional/path/to/test/file.py>
```

You can also add `-v` to see the names of the tests being run.

To check test coverage locally:

```bash
py.test --cov=loris --cov-report html:cov_html
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

## JPEG2000 Support

Kakadu binaries are included in this repository for testing purposes, however, JPEG2000 support is provided via OpenJpeg by default. This results  considerably worse performance, but clearer licensing terms than defaulting to Kakadu. Please review the [Kakadu Downloadable Executables Copyright and Disclaimer](https://github.com/jpstroop/loris-redux/blob/master/LICENSE-KAKADU) and the [licensing terms for OpenJPEG](https://github.com/jpstroop/loris-redux/blob/master/LICENSE-OPENJPEG). To configure Kakadu, acquire and install a the Kakadu binaries, and replace the OpenJpeg transcoder configuration in the application config with:

```yaml
transcoders:
 # ....
  - class: loris.transcoders.kakadu_jp2_transcoder.KakaduJp2Transcoder
    bin: /absolute/path/to/kdu_expand
    lib: /absolute/path/to/THE_DIRECTORY_THAT_CONTAINS_libkdu_vXX.so
    src_format: jp2
```
