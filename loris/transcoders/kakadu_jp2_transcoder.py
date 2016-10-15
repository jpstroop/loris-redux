from logging import getLogger
from os.path import abspath
from os.path import dirname
from os.path import join
import platform

from loris.constants import FULL
from loris.transcoders.api import AbstractTranscoder
from loris.transcoders.jp2_transcoder_helpers_mixin import Jp2TranscoderHelpersMixin

LINUX_KDU_BIN = 'kdu_expand'
LINUX_KDU_LIB = 'libkdu_v78R.so'

logger = getLogger('loris')

class KakaduJp2Transcoder(AbstractTranscoder, Jp2TranscoderHelpersMixin):

    def __init__(self, config):
        Jp2TranscoderHelpersMixin.__init__(self, config)
        AbstractTranscoder.__init__(self, config)
        if self.lib is None or self.bin is None:
            self.lib, self.bin = KakaduJp2Transcoder._find_kakadu()

    def execute(self, image_request):
        # TODO: build command and use:
        # Jp2TranscoderHelpersMixin.execute_shellout(cmd, image_request)
        pass

    def _build_command(self, image_request):
        region_param = KakaduJp2Transcoder.region_from_image_request(image_request)
        reduce_param = KakaduJp2Transcoder.reduce_from_image_request(image_request)
        return '"{0}"'.format(' '.join((self.bin, region_param, reduce_param)))

    @staticmethod
    def region_from_image_request(image_request):
        # Analogous to opj_decompress -d, but works w/ decimals and expects the
        # y & height dimensions first: {<top>,<left>},{<height>,<width>}
        if image_request.region_param.request_type is FULL:
            return ''
        else:
            top = image_request.region_decimal_y
            left = image_request.region_decimal_x
            height = image_request.region_decimal_h
            width = image_request.region_decimal_w
            template = '-region {{{0},{1}}},{{{2},{3}}}'
            return template.format(top, left, height, width)

    @staticmethod
    def reduce_from_image_request(image_request):
        arg = KakaduJp2Transcoder.reduce_arg_from_image_request(image_request)
        return '-reduce {0}'.format(arg)

    @staticmethod
    def _find_kakadu():
        system = platform.system().lower()
        processor = platform.processor() # this may need be made more specifc
        project_dir = dirname(dirname(dirname(abspath(__file__))))
        kdu_dir = join(project_dir, 'tests', 'kakadu', system, processor)
        if system == 'linux':
            return (join(kdu_dir, LINUX_KDU_LIB), join(kdu_dir, LINUX_KDU_BIN))
        else:
            msg = 'Kakadu binaries not included for {0}/{1}'.format(system, processor)
            raise RuntimeError(msg)
