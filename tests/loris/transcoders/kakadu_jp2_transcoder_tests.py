from loris.transcoders.kakadu_jp2_transcoder import KakaduJp2Transcoder

from decimal import Decimal
from os.path import exists
from unittest.mock import Mock

class TestKakaduJp2Transcoder(object):

    def test_it_can_find_kakadu(self):
        lib, binary = KakaduJp2Transcoder._find_kakadu()
        assert exists(lib)
        assert lib.endswith('.so')
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

    def test__build_command(self):
        info = Mock(width=7200, height=4128, all_scales=[1, 2, 4, 8, 16, 32, 64])
        mock_data = {
            'width' : 200,
            'height' : 118,
            'region_decimal_x' : 0,
            'region_decimal_y' : Decimal('0.17789195945'),
            'region_decimal_w' : 1,
            'region_decimal_h' : Decimal('0.64407721149'),
            'info' :  info
        }
        image_request = Mock(**mock_data)
        transcoder = KakaduJp2Transcoder({})
        cmd_no_path = 'kdu_expand -region {0.17789195945,0},{0.64407721149,1} -reduce 5"'
        assert transcoder._build_command(image_request).endswith(cmd_no_path)
