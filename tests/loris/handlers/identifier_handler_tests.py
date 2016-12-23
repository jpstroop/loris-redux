from tests.loris.handlers.base_handler_test import BaseHandlerTest

class TestIdentifierHandler(BaseHandlerTest):

    def test_base_id_redirects(self):
        self.getPage('/nir%2fvana')
        self.assertStatus(303)
        self.assertHeader('Location', '/nir%2Fvana/info.json')
