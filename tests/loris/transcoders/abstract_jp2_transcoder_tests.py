from loris.transcoders.abstract_jp2_transcoder import AbstractJp2Transcoder
from unittest.mock import Mock
import os
import stat


class TestAbstractJp2Transcoder(object):
    def test__named_pipe(self):
        class ActualJp2Transcoder(AbstractJp2Transcoder):
            def _build_command(self, image_request, fifo_path):
                pass

        transcoder = ActualJp2Transcoder({})
        with transcoder._named_pipe() as pipe_path:
            fifo_path = transcoder._named_pipe()
            assert stat.S_ISFIFO(os.stat(pipe_path).st_mode)
            assert pipe_path.endswith(".bmp")
        assert not os.path.exists(pipe_path)

    def test__get_closest_scale(self):
        req_w = 300
        req_h = 400
        full_w = 6000
        full_h = 8000
        scales = [1, 2, 4, 8, 16, 32, 64]
        meth = AbstractJp2Transcoder._get_closest_scale
        assert meth(req_w, req_h, full_w, full_h, scales) == 16

    def test__get_closest_scale_empty_returns_1(self):
        req_w = 300
        req_h = 400
        full_w = 6000
        full_h = 8000
        scales = []
        meth = AbstractJp2Transcoder._get_closest_scale
        assert meth(req_w, req_h, full_w, full_h, scales) == 1

    def test__scales_to_reduce_arg(self):
        req_w = 300
        req_h = 400
        full_w = 5999
        full_h = 7600
        scales = [1, 2, 4, 8, 16, 32, 64]
        meth = AbstractJp2Transcoder._scales_to_reduce_arg
        assert meth(req_w, req_h, full_w, full_h, scales) == "4"

    def test__scales_to_reduce_arg_no_scales_returns_0(self):
        req_w = 300
        req_h = 400
        full_w = 5999
        full_h = 7600
        scales = []
        meth = AbstractJp2Transcoder._scales_to_reduce_arg
        assert meth(req_w, req_h, full_w, full_h, scales) == "0"

    def test_reduce_arg_from_image_request_portrait(self):
        # Mock
        info = Mock(width=5000, height=6500, all_scales=[1, 2, 4, 8, 16, 32, 64])
        args = {
            "width": 250,  # can discard 4 (312px)
            "height": 400,  # can discard 4 (407px)
            "info": info,
        }
        image_request = Mock(**args)
        meth = AbstractJp2Transcoder.reduce_arg_from_image_request
        assert meth(image_request) == "4"

    def test_reduce_arg_from_image_request_landscape(self):
        # Mock
        info = Mock(width=7200, height=4128, all_scales=[1, 2, 4, 8, 16, 32, 64])
        args = {
            "width": 200,  # can discard 5 (225px)
            "height": 118,  # can discard 5 (129px)
            "info": info,
        }
        image_request = Mock(**args)
        meth = AbstractJp2Transcoder.reduce_arg_from_image_request
        assert meth(image_request) == "5"
