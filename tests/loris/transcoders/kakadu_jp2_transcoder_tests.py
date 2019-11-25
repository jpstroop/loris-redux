from decimal import Decimal
from os.path import exists
from os.path import isdir
from unittest.mock import Mock

import pytest

from loris.constants import FULL
from loris.constants import SIZE_BY_W
from loris.transcoders.kakadu_jp2_transcoder import KakaduJp2Transcoder

from tests.loris.transcoders.helpers import BLUE
from tests.loris.transcoders.helpers import GREEN
from tests.loris.transcoders.helpers import ORANGE
from tests.loris.transcoders.helpers import RED
from tests.loris.transcoders.helpers import is_close_color
from tests.loris.transcoders.helpers import tmp_image

@pytest.fixture(scope='module')
def transcoder():
    return KakaduJp2Transcoder({})

class TestKakaduJp2Transcoder(object):

    def test_it_can_find_kakadu(self):
        lib, binary = KakaduJp2Transcoder._find_kakadu()
        assert exists(lib)
        assert isdir(lib)
        assert exists(binary)

    def test_region_from_image_request(self):
        args = {
            'region_decimal_x' : 0,
            'region_decimal_y' : Decimal('0.1778919594500763782807943341'),
            'region_decimal_w' : 1,
            'region_decimal_h' : Decimal('0.6440772114984029995833911957')
        }
        image_request = Mock(**args)
        meth = KakaduJp2Transcoder.region_from_image_request
        expected = '-region {0.1778919594500763782807943341,0},{0.6440772114984029995833911957,1}'
        assert meth(image_request) == expected

    def test_reduce_from_image_request(self):
        info = Mock(width=7200, height=4128, all_scales=[1, 2, 4, 8, 16, 32, 64])
        args = {
            'width' : 200, # can discard 5 (225px)
            'height' : 118, # can discard 5 (129px)
            'info' :  info
        }
        image_request = Mock(**args)
        meth = KakaduJp2Transcoder.reduce_from_image_request
        assert meth(image_request) == '-reduce 5'

    def test__build_command(self, transcoder):
        info = Mock(width=7200, height=4128, all_scales=[1, 2, 4, 8, 16, 32, 64])
        mock_data = {
            'width' : 200,
            'height' : 118,
            'region_decimal_x' : 0,
            'region_decimal_y' : Decimal('0.17789195945'),
            'region_decimal_w' : 1,
            'region_decimal_h' : Decimal('0.64407721149'),
            'info' :  info,
            'file_path' : '/foo/bar.jp2'
        }
        image_request = Mock(**mock_data)
        fake_pipe = '/baz/quux.bmp'
        cmd_no_path = 'kdu_expand -i /foo/bar.jp2 -o /baz/quux.bmp -region {0.17789195945,0},{0.64407721149,1} -reduce 5'
        assert transcoder._build_command(image_request, fake_pipe).endswith(cmd_no_path)

    def test__execute_simple(self, transcoder, region_test_jp2):
        # This is the equivalent of /full/full/0/default.jpg.
        # It will be slow (~2-2.5 seconds)
        image_request = Mock(
            info = Mock(
                width=6000,
                height=8000,
                all_scales=[1, 2, 4, 8, 16, 32, 64]
            ),
            file_path = region_test_jp2,
            region_request_type = FULL, # _region_param.request_type
            region_decimal_x = 0,       # _region_param.decimal_x
            region_decimal_y = 0,       # _region_param.decimal_y
            region_decimal_w = 1,       # _region_param.decimal_w
            region_decimal_h = 1,       # _region_param.decimal_h
            size_request_type = FULL,   # _size_param.request_type
            width = 6000,               # _size_param.width
            height = 8000,              # _size_param.height
            mirror = False,             # _rotation_param.mirror
            rotation = 0.0,             # _rotation_param.rotation
            quality = 'default',        # _quality_param.canonical
            format = 'jpg'              # _format_param.canonical
        )
        stream = transcoder.execute(image_request)
        with tmp_image(stream) as i:
            assert i.size == (6000, 8000)
            assert is_close_color(i.getpixel((0,0)), GREEN)
            assert is_close_color(i.getpixel((5999,0)), RED)
            assert is_close_color(i.getpixel((0,7999)), BLUE)
            assert is_close_color(i.getpixel((5999,7999)), ORANGE)

    def test__execute_small_full(self, transcoder, region_test_jp2):
        # This is the equivalent of /full/3000,/0/default.jpg.
        image_request = Mock(
            info = Mock(
                width=6000,
                height=8000,
                all_scales=[1, 2, 4, 8, 16, 32, 64]
            ),
            file_path = region_test_jp2,
            region_request_type = FULL,    # _region_param.request_type
            region_decimal_x = 0,          # _region_param.decimal_x
            region_decimal_y = 0,          # _region_param.decimal_y
            region_decimal_w = 1,          # _region_param.decimal_w
            region_decimal_h = 1,          # _region_param.decimal_h
            size_request_type = SIZE_BY_W, # _size_param.request_type
            width = 60,                    # _size_param.width
            height = 80,                   # _size_param.height
            mirror = False,                # _rotation_param.mirror
            rotation = 0.0,                # _rotation_param.rotation
            quality = 'default',           # _quality_param.canonical
            format = 'png'                 # _format_param.canonical
        )
        stream = transcoder.execute(image_request)
        with tmp_image(stream) as i:
            assert i.size == (60, 80)
            assert i.format == 'PNG'
