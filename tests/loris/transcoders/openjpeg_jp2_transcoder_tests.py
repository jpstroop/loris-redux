from loris.transcoders.openjpeg_jp2_transcoder import OpenJpegJp2Transcoder

from os.path import exists
from unittest.mock import Mock

class TestOpenJpegJp2Transcoder(object):

    def test_it_can_find_openjpeg(self):
        lib, binary = OpenJpegJp2Transcoder._find_openjpeg()
        assert exists(lib)
        assert lib.endswith('.so.2.1.2')
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
        assert meth(image_request) == '-d 0,1024,512,512'

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

    def test__build_command(self):
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
        transcoder = OpenJpegJp2Transcoder({})
        fake_pipe = '/baz/quux.bmp'
        cmd_no_path = 'opj_decompress -i /foo/bar.jp2 -o /baz/quux.bmp -d 0,1024,512,512 -r 4"'
        assert transcoder._build_command(image_request, fake_pipe).endswith(cmd_no_path)
