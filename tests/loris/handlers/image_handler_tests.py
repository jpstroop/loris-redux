from tests.loris.handlers.base_handler_test import BaseHandlerTest

from json import loads
from sys import version_info

PYTHON_VERSION = '.'.join(map(str, version_info[0:3]))

class TestImageHandler(BaseHandlerTest):


    def test_image_returns200(self):
        uri = '/loris:sample.jp2/full/200,/0/default.jpg'
        status, headers, body = self.getPage(uri)
        self.assertStatus(200)

    def test_image_headers(self):
        uri = '/loris:sample.jp2/full/200,/0/default.jpg'
        status, headers, body = self.getPage(uri)
        headers = dict(headers)
        assert 'Etag' in headers
        self.assertHeader('Allow', 'GET')
        self.assertHeader('Content-Type', 'image/jpeg')
        if PYTHON_VERSION == '3.5.2':
            self.assertHeader('Content-Length', '5962') # careful, this could change
        elif PYTHON_VERSION == '3.6.0': # not sure why, but everything seems fine
            self.assertHeader('Content-Length', '5904')

    def test_redirect_to_canonical(self):
        uri = '/loris:sample.jp2/full/pct:5/0/default.jpg'
        self.getPage(uri)
        self.assertHeader('Location', '/loris:sample.jp2/full/300,/0/default.jpg')

    def test_etag_works(self):
        uri = '/loris:sample.jp2/full/200,/0/default.jpg'
        headers = self.getPage(uri)[1]
        etag = dict(headers)['Etag']
        self.getPage(uri, headers=[('if-none-match', etag)])
        self.assertStatus(304)

    def test_400_for_bad_syntax(self):
        uri = '/loris:sample.jp2/full/pct:10,/0/default.jpg'
        status, body  = self.getPage(uri)[0::2]
        body = loads(body.decode('utf-8'))
        self.assertStatus(400)
        assert body['error'] == 'SyntaxException'
        assert body['description'] == "could not convert string to float: '10,'"
