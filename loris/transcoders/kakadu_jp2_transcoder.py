from os.path import abspath
from os.path import dirname
from os.path import join
import platform

from loris.transcoders.api import AbstractTranscoder
from loris.transcoders.jp2_transcoder_helpers_mixin import Jp2TranscoderHelpersMixin

LINUX_KDU_BIN = 'kdu_expand'
LINUX_KDU_LIB = 'libkdu_v78R.so'

class KakaduJp2Transcoder(AbstractTranscoder, Jp2TranscoderHelpersMixin):

    def __init__(self, config):
        Jp2TranscoderHelpersMixin.__init__(self)
        AbstractTranscoder.__init__(self, config)

        if self.lib is None or self.bin is None:
            self.lib, self.bin = KakaduJp2Transcoder._find_kakadu()

    @staticmethod
    def _find_kakadu():
        system = platform.system().lower()
        processor = platform.processor() # this may need be made more specifc
        project_dir = dirname(dirname(dirname(abspath(__file__))))
        kdu_dir = join(project_dir, 'kakadu', system, processor)
        if system == 'linux':
            return (join(kdu_dir, LINUX_KDU_LIB), join(kdu_dir, LINUX_KDU_BIN))
        else:
            msg = 'Kakadu binaries not included for {0} system'.format(system)
            raise RuntimeError(msg)
