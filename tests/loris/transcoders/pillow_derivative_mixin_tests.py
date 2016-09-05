from loris.transcoders.pillow_derivative_mixin import PillowDerviativeMixin
from loris.transcoders.api import AbstractTranscoder
import inspect

class TestPillowDerivativeMixin(object):

    def test_can_be_mixed_with_abstract_transcoder(self):
        class MyTranscoder(AbstractTranscoder, PillowDerviativeMixin):
            def __init__(self, config):
                super(MyTranscoder, self).__init__(config)
            def execute(self, image_request):
                return None # for now

        transcoder = MyTranscoder({})
        assert hasattr(transcoder, 'derive')
        assert inspect.isfunction(MyTranscoder.derive)
