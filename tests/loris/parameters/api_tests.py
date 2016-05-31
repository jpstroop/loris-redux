from loris.parameters.api import AbstractParameter
import pytest

class ProperImpl(AbstractParameter):
    def __init__(self, uri_slice):
        super(ProperImpl, self).__init__(uri_slice)
    @property
    def canonical(self):
        return 'canonical version'

class TestAbstractParameter(object):

    def test_canonical_required(self):
        class WithoutCanonical(AbstractParameter):
            def __init__(self, uri_slice):
                super(WithoutCanonical, self).__init__(uri_slice)
        with pytest.raises(TypeError) as type_error:
            w = WithoutCanonical('abc')
        assert "Can't instantiate abstract class" in str(type_error.value)


    def test_init_required(self):
        class WithoutInit(AbstractParameter):
            @property
            def canonical(self):
                return 'canonical version'
        with pytest.raises(TypeError) as type_error:
            w = WithoutInit('abc')
        assert "Can't instantiate abstract class" in str(type_error.value)

    def test_init_sig_required(self):
        class WrongInitSig(AbstractParameter):
            def __init__(self):
                super(WrongInitSig, self).__init__()
            @property
            def canonical(self):
                return 'canonical version'
        with pytest.raises(TypeError) as type_error:
            w = WrongInitSig()
        assert "__init__() missing 1 required positional" in str(type_error.value)

    def test_proper_impl(self):
        p = ProperImpl('foo')

    def test_original_request_is_defined(self):
        p = ProperImpl('foo')
        assert p.original_request == 'foo'

    def test_canonical_must_be_property(self):
        pass
        # TODO: How?
        # class CanonicalNotProperty(AbstractParameter):
        #     def __init__(self, uri_slice):
        #         super(CanonicalNotProperty, self).__init__(uri_slice)
        #     def canonical(self):
        #         return 'canonical version'
        # with pytest.raises(TypeError) as type_error:
        #     w = CanonicalNotProperty('foo')
