# loris-redux

[![Build Status](https://travis-ci.org/jpstroop/loris-redux.svg?branch=master)](https://travis-ci.org/jpstroop/loris-redux) [![Coverage Status](https://coveralls.io/repos/github/jpstroop/loris-redux/badge.svg?branch=master)](https://coveralls.io/github/jpstroop/loris-redux?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/ffde55935b8967cd546a/maintainability)](https://codeclimate.com/github/jpstroop/loris-redux/maintainability) [![Requirements Status](https://requires.io/github/jpstroop/loris-redux/requirements.svg)](https://requires.io/github/jpstroop/loris-redux/requirements/)

[![License: New BSD](https://img.shields.io/badge/license-New%20BSD-blue.svg)](https://github.com/jpstroop/loris-redux/blob/master/LICENSE)

[![Python 3.7](https://img.shields.io/badge/python-3.7-yellow.svg)](https://img.shields.io/badge/python-3.7-yellow.svg)
[![Python 3.8](https://img.shields.io/badge/python-3.8-yellow.svg)](https://img.shields.io/badge/python-3.8-yellow.svg)
[![Python Nightly](https://img.shields.io/badge/python-nightly-yellow.svg)](https://img.shields.io/badge/python-nightly-yellow.svg)

A rewrite of loris using [CherryPy](http://cherrypy.org/) and Python `>=` 3.7.

## Running the Application and Tests

Not for Production! Also, this assumes you have [pipenv](https://pipenv.kennethreitz.org/en/latest/) installed.

Install the Appllication

```bash
$ brew install libmagic # on macOS only
$ pipenv install --dev --python [path to python >=3.7.0]  # --dev assumes you'll want to run tests
```

Run the Server in debug mode

```bash
$ pipenv run python run.py
```

 * Info: `http://localhost:5004/loris:sample.jp2/info.json`
 * Pixels: `http://localhost:5004/loris:sample.jp2/full/800,/0/default.jpg`

There is also an extension service, `/resolvers.json` that lists the available resolvers. This is still WIP (see [#101](https://github.com/jpstroop/loris-redux/issues/101)), but the concept is there.

Run tests

```bash
$ pipenv run pytest
```

If you want to see logging output while running the tests, run them with pytest:

```bash
$ pipenv run py.test -s <optional/path/to/test/file.py>
```

You can also add `-v` to see the names of the tests being run. [Pytest has a lot of options](http://doc.pytest.org/en/latest/usage.html).

To check test coverage locally:

```bash
pipenv run pytest --cov=loris --cov-report html:cov_html
```

## IIIF Compliance

All [IIIF Image API 3.0 features](https://iiif.io/api/image/3.0/compliance/) are implemented. These can be enabled and disabled in [`loris/config.yaml`](loris/config.yaml). The server will set the compliance level accordingly, and raise exceptions/sent the appropriate HTTP error responses for the disabled features. Level 0 is always supported.

There is a non-standard option to support just tiles and scale factors at an otherwise level 0 compliance. This is enabled and configured in the `application` section of [`loris/config.yaml`](loris/config.yaml).

## JPEG2000 Support

Kakadu binaries [are included in this repository](https://github.com/jpstroop/loris-redux/tree/master/tests/kakadu) __for testing purposes__, however, JPEG2000 support is provided using [OpenJpeg](http://www.openjpeg.org/) by default. This results  considerably worse performance, but clearer licensing terms. Please review the [Kakadu Downloadable Executables Copyright and Disclaimer](https://github.com/jpstroop/loris-redux/blob/master/LICENSE#L75) and the [licensing terms for OpenJPEG](https://github.com/jpstroop/loris-redux/blob/master/LICENSE#L33). To configure Kakadu, [acquire and install the Kakadu binaries](http://kakadusoftware.com/), and replace the OpenJpeg transcoder configuration in the application config with:

```yaml
transcoders:
 # ....
  - class: loris.transcoders.kakadu_jp2_transcoder.KakaduJp2Transcoder
    bin: /absolute/path/to/kdu_expand
    lib: /absolute/path/to/THE_DIRECTORY_THAT_CONTAINS_libkdu_vXX.so
    src_format: jp2
```

## Style

```
pipenv run black -t py37 -l 99 loris tests
```
