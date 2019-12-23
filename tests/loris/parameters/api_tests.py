from loris.parameters.api import AbstractParameter
from unittest.mock import Mock
import pytest


class ProperImpl(AbstractParameter):
    def __init__(self, uri_slice, enabled_features):
        super(ProperImpl, self).__init__(uri_slice, enabled_features)

    @property
    def canonical(self):
        return "canonical version"


class TestAbstractParameter(object):
    def test_canonical_required(self):
        class WithoutCanonical(AbstractParameter):
            def __init__(self, uri_slice, enabled_features):
                super(WithoutCanonical, self).__init__(uri_slice, enabled_features)

        with pytest.raises(TypeError) as type_error:
            w = WithoutCanonical("abc", (), Mock())
        assert "Can't instantiate abstract class" in str(type_error.value)

    def test_init_required(self):
        class WithoutInit(AbstractParameter):
            @property
            def canonical(self):
                return "canonical version"

        with pytest.raises(TypeError) as type_error:
            w = WithoutInit("abc", (), Mock())
        assert "Can't instantiate abstract class" in str(type_error.value)

    def test_init_sig_required(self):
        class WrongInitSig(AbstractParameter):
            def __init__(self):
                super(WrongInitSig, self).__init__()

            @property
            def canonical(self):
                return "canonical version"

        with pytest.raises(TypeError) as type_error:
            WrongInitSig()
        assert "__init__() missing 2 required positional" in str(type_error.value)

    def test_proper_impl(self):
        ProperImpl("foo", ())

    def test_stuff_is_defined(self):
        p = ProperImpl("foo", ())
        assert p.uri_slice == "foo"
        assert p.enabled_features == ()
