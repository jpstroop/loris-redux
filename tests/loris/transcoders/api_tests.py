from loris.transcoders.api import AbstractTranscoder
import pytest

class ProperImpl(AbstractTranscoder):
    def __init__(self, config):
        super(ProperImpl, self).__init__(config)
    def transcode(self):
        return None # for now

class TestAbstractTranscoder(object):

    def test_transcode_required(self):
        class WithoutTranscode(AbstractTranscoder):
            def __init__(self, config):
                super(WithoutTranscode, self).__init__(config)
        with pytest.raises(TypeError) as type_error:
            w = WithoutTranscode({ 'foo' : 'bar'})
        assert "Can't instantiate abstract class" in str(type_error.value)

    def test_no_need_to_impl_init(self):
        # though you'll probably almost always want to
        class NoInitImpl(AbstractTranscoder):
            def transcode(self):
                return None # for now
        transcoder = NoInitImpl()

    def test_proper_impl_works(self):
        transcoder = ProperImpl({})

    def test_arbirtary_configs_added_to_instance(self):
        transcoder = ProperImpl({'foo' : 'bar'})
        assert transcoder.foo == 'bar'
