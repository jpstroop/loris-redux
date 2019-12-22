from logging import getLogger
from loris.constants import KEYWORD_FULL
from loris.transcoders.abstract_jp2_transcoder import AbstractJp2Transcoder
from loris.transcoders.api import AbstractTranscoder
from os.path import abspath
from os.path import dirname
from os.path import join
import platform

LINUX_KDU_BIN = 'kdu_expand'

logger = getLogger('loris')

class KakaduJp2Transcoder(AbstractJp2Transcoder, AbstractTranscoder):

    def __init__(self, config):
        AbstractTranscoder.__init__(self, config)
        AbstractJp2Transcoder.__init__(self, config)
        self.lib_dir, self.bin = KakaduJp2Transcoder._find_kakadu()
        self.env = {
            'LD_LIBRARY_PATH' : self.lib_dir,
            'PATH' : self.bin
        }

    def _build_command(self, image_request, fifo_path):
        i_param = f'-i {image_request.file_path}'
        o_param = f'-o {fifo_path}'
        reg_param = KakaduJp2Transcoder.region_from_image_request(image_request)
        red_param = KakaduJp2Transcoder.reduce_from_image_request(image_request)
        return f'{self.bin} {i_param} {o_param} {reg_param} {red_param}'

    @staticmethod
    def region_from_image_request(image_request):
        # Analogous to opj_decompress -d, but works w/ decimals and expects the
        # y & height dimensions first: {<top>,<left>},{<height>,<width>}

        if image_request.region_request_type is KEYWORD_FULL:
            return ''
        else:
            top = image_request.region_decimal_y
            left = image_request.region_decimal_x
            height = image_request.region_decimal_h
            width = image_request.region_decimal_w
            return f'-region {{{top},{left}}},{{{height},{width}}}'

    @staticmethod
    def reduce_from_image_request(image_request):
        arg = KakaduJp2Transcoder.reduce_arg_from_image_request(image_request)
        return f'-reduce {arg}'

    @staticmethod
    def _find_kakadu(): # THIS IS ONLY MEANT FOR TESTS. SUPPLY YOUR OWN!
        system = platform.system().lower()
        processor = platform.processor() # this may need be made more specifc
        project_dir = dirname(dirname(dirname(abspath(__file__))))
        kdu_dir = join(project_dir, 'tests', 'kakadu', system, processor)
        if system in ('linux','darwin'):
            return (kdu_dir, join(kdu_dir, LINUX_KDU_BIN))
        else:
            msg = f'Kakadu binaries not included for {system}/{processor}'
            raise RuntimeError(msg)
