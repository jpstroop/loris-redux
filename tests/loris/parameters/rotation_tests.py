from decimal import Decimal
from loris.exceptions.request_exception import RequestException
from loris.exceptions.syntax_exception import SyntaxException
from loris.exceptions.feature_not_enabled_exception import FeatureNotEnabledException
from loris.parameters.rotation import RotationParameter

import pytest

class TestRotationParameter(object):

    def test_zero_is_fine(self):
        uri_slice = '0'
        features = ()
        rp = RotationParameter(uri_slice, features)
        assert rp.rotation == 0.0
        assert rp.canonical == '0'
        assert not rp.mirror

    def test_mirror_0_is_fine(self):
        uri_slice = '!0'
        features = ('mirroring')
        rp = RotationParameter(uri_slice, features)
        assert rp.rotation == 0.0
        assert rp.canonical == '!0'
        assert rp.mirror

    def test_mirror_wo_enabled_will_raise(self):
        uri_slice = '!0'
        features = ()
        with pytest.raises(FeatureNotEnabledException) as fe:
            RotationParameter(uri_slice, features)
        assert "not support the 'mirroring' feature" in fe.value.message

    def test_regex_will_raise(self):
        uri_slice = '@0'
        features = ()
        with pytest.raises(SyntaxException) as se:
            RotationParameter(uri_slice, features)
        assert 'Could not parse region request (@0)' == se.value.message

    def test_rotation_by_90s_ok(self):
        uri_slice = '90'
        features = ('rotationBy90s')
        rp = RotationParameter(uri_slice, features)
        assert rp.rotation == 90.0
        assert rp.canonical == '90'
        assert not rp.mirror

    def test_rotation_by_90s_mirror_ok(self):
        uri_slice = '!270'
        features = ('rotationBy90s', 'mirroring')
        rp = RotationParameter(uri_slice, features)
        assert rp.rotation == 270.0
        assert rp.canonical == '!270'
        assert rp.mirror

    def test_rotation_by_90s_wo_enabled_raises(self):
        uri_slice = '90'
        features = ()
        with pytest.raises(FeatureNotEnabledException) as fe:
            RotationParameter(uri_slice, features)
        assert "not support the 'rotationBy90s' feature" in fe.value.message

    def test_rotation_arbitrary_wo_enabled_raises(self):
        uri_slice = '92.3'
        features = ()
        with pytest.raises(FeatureNotEnabledException) as fe:
            RotationParameter(uri_slice, features)
        assert "not support the 'rotationArbitrary' feature" in fe.value.message

    def test_rotation_arbitrary_ok(self):
        uri_slice = '92.3'
        features = ('rotationArbitrary')
        rp = RotationParameter(uri_slice, features)
        assert rp.rotation == 92.3
        assert rp.canonical == '92.3'
        assert not rp.mirror
