from tests.loris.handlers.base_handler_test import BaseHandlerTest

from json import loads

class TestResolversHandler(BaseHandlerTest):

    def test_resolvers_redirects(self):
        self.getPage('/resolvers')
        self.assertStatus(303)
        self.assertHeader('Location', '/resolvers.json')

    def test_resolvers_json_includes_sample_resolver(self):
        status, headers, body = self.getPage('/resolvers.json')
        self.assertStatus(200)
        self.assertHeader('Content-type', 'application/json')
        resolver_list = loads(body.decode('utf-8'))
        assert any([entry['prefix'] == 'loris' for entry in resolver_list])
