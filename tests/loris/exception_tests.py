from loris.exceptions import LorisException
from loris.exceptions import ResolverException

class TestLorisException(object):

    def test_to_json(self):
        message = 'the message'
        ex = LorisException(message, 400)
        j = '{"error": "LorisException", "description": "the message"}'
        assert ex.to_json() == j
        assert str(ex) == j

    def test_to_json_works_on_subclasses(self):
        m = 'Could not resolve identifier: 1234'
        ex = ResolverException('1234')
        j = '{{"error": "ResolverException", "description": "{0}"}}'.format(m)
        assert ex.to_json() == j
        assert str(ex) == j
