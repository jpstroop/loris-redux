from os.path import abspath
from os.path import dirname
from os.path import join
import platform

from loris.transcoders.api import AbstractTranscoder
from loris.transcoders.jp2_transcoder_helpers_mixin import Jp2TranscoderHelpersMixin


LINUX_OPJ_BIN = 'opj_decompress'
LINUX_OPJ_LIB = 'libopenjp2.so.2.1.2'

class OpenJpegJp2Transcoder(AbstractTranscoder, Jp2TranscoderHelpersMixin):

    def __init__(self, config):
        Jp2TranscoderHelpersMixin.__init__(self)
        AbstractTranscoder.__init__(self, config)
        if self.lib is None or self.bin is None:
            self.lib, self.bin = OpenJpegJp2Transcoder._find_openjpeg()

    @staticmethod
    def _find_openjpeg():
        system = platform.system().lower()
        processor = platform.processor() # is this enough?
        package_dir = dirname(dirname(abspath(__file__)))
        opj_dir = join(package_dir, 'openjpeg', system, processor)
        if system == 'linux':
            return (join(opj_dir, LINUX_OPJ_LIB), join(opj_dir, LINUX_OPJ_BIN))
        else:
            msg = 'OpenJpeg binaries not included for {0} system'.format(system)
            raise RuntimeError(msg)
