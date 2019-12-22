from os.path import exists
from os.path import isdir
from unittest.mock import Mock

import pytest

from loris.constants import KEYWORD_FULL
from loris.constants import FEATURE_SIZE_BY_W
from loris.transcoders.openjpeg_jp2_transcoder import OpenJpegJp2Transcoder

from tests.loris.transcoders.helpers import BLUE
from tests.loris.transcoders.helpers import GREEN
from tests.loris.transcoders.helpers import ORANGE
from tests.loris.transcoders.helpers import RED
from tests.loris.transcoders.helpers import is_close_color
from tests.loris.transcoders.helpers import tmp_image

@pytest.fixture(scope='module')
def transcoder():
    return OpenJpegJp2Transcoder({})

class TestOpenJpegJp2Transcoder(object):

    def test_it_can_find_openjpeg(self):
        lib, binary = OpenJpegJp2Transcoder._find_openjpeg()
        assert exists(lib)
        assert isdir(lib)
        assert exists(binary)

    def test_decode_area_from_image_request(self):
        args = {
            'region_pixel_x' : 0,
            'region_pixel_y' : 1024,
            'region_pixel_w' : 512,
            'region_pixel_h' : 512
        }
        image_request = Mock(**args)
        meth = OpenJpegJp2Transcoder.decode_area_from_image_request
        assert meth(image_request) == '-d 0,1024,512,1536'

    def test_reduce_from_image_request(self):
        info = Mock(width=5000, height=6500, all_scales=[1, 2, 4, 8, 16, 32, 64])
        args = {
            'width' : 250,
            'height' : 400,
            'info' : info
        }
        image_request = Mock(**args)
        meth = OpenJpegJp2Transcoder.reduce_from_image_request
        assert meth(image_request) == '-r 4'

    def test__build_command(self, transcoder):
        info = Mock(width=5000, height=6500, all_scales=[1, 2, 4, 8, 16, 32, 64])
        mock_data = {
            'width' : 250,
            'height' : 400,
            'region_pixel_x' : 0,
            'region_pixel_y' : 1024,
            'region_pixel_w' : 512,
            'region_pixel_h' : 512,
            'info' :  info,
            'file_path' : '/foo/bar.jp2'
        }
        image_request = Mock(**mock_data)
        fake_pipe = '/baz/quux.bmp'
        cmd_no_path = 'opj_decompress -i /foo/bar.jp2 -o /baz/quux.bmp -d 0,1024,512,1536 -r 4'
        assert transcoder._build_command(image_request, fake_pipe).endswith(cmd_no_path)

    @pytest.mark.filterwarnings("ignore:unclosed file")
    def test__execute_small_full(self, transcoder, region_test_jp2):
        # This is the equivalent of /full/full/0/default.jpg.
        # It will be slow (~2-2.5 seconds)
        image_request = Mock(
            info = Mock(
                width=6000,
                height=8000,
                all_scales=[1, 2, 4, 8, 16, 32, 64]
            ),
            file_path = region_test_jp2,
            region_request_type = KEYWORD_FULL, # _region_param.request_type
            region_pixel_x = 0,         # _region_param.pixel_x
            region_pixel_y = 0,         # _region_param.pixel_y
            region_pixel_w = 60,        # _region_param.pixel_w
            region_pixel_h = 80,        # _region_param.pixel_h
            size_request_type = FEATURE_SIZE_BY_W,  # _size_param.request_type
            width = 60,                 # _size_param.width
            height = 80,                # _size_param.height
            mirror = False,             # _rotation_param.mirror
            rotation = 0.0,             # _rotation_param.rotation
            quality = 'default',        # _quality_param.canonical
            format = 'jpg'              # _format_param.canonical
        )
        stream = transcoder.execute(image_request)
        with tmp_image(stream) as i:
            # i.show() # helpful
            assert i.size == (60, 80)
            assert is_close_color(i.getpixel((0,0)), GREEN)
            assert is_close_color(i.getpixel((59,0)), RED)
            assert is_close_color(i.getpixel((0,79)), BLUE)
            assert is_close_color(i.getpixel((59,79)), ORANGE)
