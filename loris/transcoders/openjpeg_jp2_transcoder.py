from logging import getLogger
from os.path import abspath
from os.path import dirname
from os.path import join
import platform

from loris.constants import FULL
from loris.transcoders.api import AbstractTranscoder
from loris.transcoders.abstract_jp2_transcoder import AbstractJp2Transcoder

OPJ_DECOMPRESS = 'opj_decompress'

logger = getLogger('loris')

class OpenJpegJp2Transcoder(AbstractJp2Transcoder, AbstractTranscoder):

    def __init__(self, config):
        AbstractTranscoder.__init__(self, config)
        AbstractJp2Transcoder.__init__(self, config)
        self.lib_dir, self.bin = OpenJpegJp2Transcoder._find_openjpeg()
        self.env = {
            'LD_LIBRARY_PATH' : self.lib_dir,   # for linux
            'DYLD_LIBRARY_PATH' : self.lib_dir, # for darwin
            'PATH' : self.bin
        }

    def _build_command(self, image_request, fifo_path):
        i_param = '-i {0}'.format(image_request.file_path)
        o_param = '-o {0}'.format(fifo_path)
        d_param = OpenJpegJp2Transcoder.decode_area_from_image_request(image_request)
        r_param = OpenJpegJp2Transcoder.reduce_from_image_request(image_request)
        cmd = ' '.join((self.bin, i_param, o_param, d_param, r_param))
        if platform.system().lower() == 'linux':
            cmd = f'"{cmd}"'
        return cmd

    @staticmethod
    def decode_area_from_image_request(image_request):
        # analogous to kdu_expand -region, but works w/ pixels
        if image_request.region_request_type is FULL:
            return ''
        else:
            x = image_request.region_pixel_x
            y = image_request.region_pixel_y
            w = image_request.region_pixel_x + image_request.region_pixel_w
            h = image_request.region_pixel_y + image_request.region_pixel_h
            return '-d {0},{1},{2},{3}'.format(x, y, w, h)

    @staticmethod
    def reduce_from_image_request(image_request):
        arg = OpenJpegJp2Transcoder.reduce_arg_from_image_request(image_request)
        return '-r {0}'.format(arg)

    @staticmethod
    def _find_openjpeg():
        system = platform.system().lower()
        processor = platform.machine() # is this enough?
        package_dir = dirname(dirname(abspath(__file__)))
        opj_dir = join(package_dir, 'openjpeg', system, processor)
        if system in ('linux', 'darwin'):
            return (opj_dir, join(opj_dir, OPJ_DECOMPRESS))
        else:
            msg = 'OpenJpeg binaries not included for for {0}/{1}'.format(system, processor)
            raise RuntimeError(msg)
