from loris.helpers.import_class import import_class

class TestImportClass(object):

    def test_it_works(self):
        # Note that this has nothing to do with unittest or MagicMock; just
        # needed a class with some package/module structure to test.
        Klass = import_class('unittest.mock.MagicMock')
        mock = Klass()
        assert Klass.__name__ == 'MagicMock'
        assert isinstance(mock, Klass)
