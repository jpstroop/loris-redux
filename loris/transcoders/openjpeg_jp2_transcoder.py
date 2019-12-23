from logging import getLogger
from loris.constants import KEYWORD_FULL
from loris.transcoders.abstract_jp2_transcoder import AbstractJp2Transcoder
from loris.transcoders.api import AbstractTranscoder
from os.path import abspath
from os.path import dirname
from os.path import join
from platform import processor
from platform import system

OPJ_BIN = "opj_decompress"

logger = getLogger("loris")


class OpenJpegJp2Transcoder(AbstractJp2Transcoder, AbstractTranscoder):
    def __init__(self, config):
        AbstractTranscoder.__init__(self, config)
        AbstractJp2Transcoder.__init__(self, config)
        self.lib_dir, self.bin = OpenJpegJp2Transcoder._find_openjpeg()
        self.env = {"LD_LIBRARY_PATH": self.lib_dir, "PATH": self.bin}

    def _build_command(self, image_request, fifo_path):
        i_param = f"-i {image_request.file_path}"
        o_param = f"-o {fifo_path}"
        d_param = OpenJpegJp2Transcoder.decode_area_from_image_request(image_request)
        r_param = OpenJpegJp2Transcoder.reduce_from_image_request(image_request)
        return f"{self.bin} {i_param} {o_param} {d_param} {r_param}"

    @staticmethod
    def decode_area_from_image_request(image_request):
        # analogous to kdu_expand -{region} but works w/ pixels
        if image_request.region_request_type is KEYWORD_FULL:
            return ""
        else:
            x = image_request.region_pixel_x
            y = image_request.region_pixel_y
            w = image_request.region_pixel_x + image_request.region_pixel_w
            h = image_request.region_pixel_y + image_request.region_pixel_h
            return f"-d {x},{y},{w},{h}"

    @staticmethod
    def reduce_from_image_request(image_request):
        arg = OpenJpegJp2Transcoder.reduce_arg_from_image_request(image_request)
        return f"-r {arg}"

    @staticmethod
    def _find_openjpeg():
        sys = system().lower()
        proc = processor()  # is this enough?
        package_dir = dirname(dirname(abspath(__file__)))
        opj_dir = join(package_dir, "openjpeg", sys, proc)
        if sys in ("linux", "darwin"):
            return (opj_dir, join(opj_dir, OPJ_BIN))
        else:
            msg = f"OpenJpeg binaries not included for for {sys}/{proc}"
            raise RuntimeError(msg)
