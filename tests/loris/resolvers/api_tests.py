from loris.resolvers.api import AbstractResolver
import pytest

class ProperImpl(AbstractResolver):
    def is_resolvable(self, ident):
        return True
    def resolve(self, ident):
        # Note that a real impl. would need to raise an IOError
        return '/foo/bar/baz.jpg'

class TestAbstractResolver(object):

    def test_is_resolvable_required(self):
        class WithoutIsResolvable(AbstractResolver):
            def resolve(self, ident):
                return '/foo/bar/baz.jpg'
            @staticmethod
            def characterize(file_path):
                return 'jpg'
        with pytest.raises(TypeError) as type_error:
            w = WithoutIsResolvable({})
        assert "Can't instantiate abstract class" in str(type_error.value)

    def test_resolvable_required(self):
        class WithoutResolvable(AbstractResolver):
            def is_resolvable(self, ident):
                return True
            @staticmethod
            def characterize(file_path):
                return 'jpg'
        with pytest.raises(TypeError) as type_error:
            w = WithoutResolvable({})
        assert "Can't instantiate abstract class" in str(type_error.value)

    def test_proper_impl_works(self):
        resolver = ProperImpl({})

    def test_arbirtary_configs_added_to_instance(self):
        config = {'foo' : 'bar', 'baz' : 'quux'}
        resolver = ProperImpl(config)
        assert resolver.foo == 'bar'
        assert resolver.baz == 'quux'
