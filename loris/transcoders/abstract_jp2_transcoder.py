from abc import ABCMeta
from abc import abstractmethod
from contextlib import contextmanager
from math import ceil
from math import log
from os import makedirs
from os import mkfifo
from os import unlink
from os.path import join
from PIL import Image
from random import choice
from string import ascii_lowercase
from subprocess import DEVNULL
from subprocess import Popen
from shlex import split

from loris.transcoders.pillow_transcoder import PillowTranscoder

class AbstractJp2Transcoder(metaclass=ABCMeta):
    # Any code that can be shared between the OpenJpegJp2Transcoder and the
    # KakaduJp2Transcoder goes here.
    def __init__(self, config):
        self.pillow_transcoder = PillowTranscoder()
        self.tmp = config.get('tmp', '/tmp/loris_tmp')
        makedirs(self.tmp, exist_ok=True) # let errors bubble up for now
        # TODO: Subclasses need to do this. Mayke them properties or something
        # so that we can be sure that they do.
        # self.lib = None
        # self.bin = None
        # self.env = {
        #     'LD_LIBRARY_PATH' : self.lib,
        #     'PATH' : self.bin
        # }

    @abstractmethod
    def _build_command(self, image_request, fifo_path):
        pass

    def execute(self, image_request):
        with self._named_pipe() as fifo_path:
            cmd = self._build_command(image_request, fifo_path)
            self._run_cmd(cmd, fifo_path)
            pillow_image = self._run_cmd(cmd, fifo_path)
        return self.pillow_transcoder.execute_with_pil_image(pillow_image, image_request)

    def _run_cmd(self, cmd, fifo_path):
        # Note: if this is causing trouble, remove stdout and stderr arg for
        # debugging
        proc = Popen(split(cmd), bufsize=-1, env=self.env)
        # proc = Popen(split(cmd), stdout=DEVNULL, stderr=DEVNULL, bufsize=-1, env=self.env)
        # THIS CAN BLOCK. See http://stackoverflow.com/q/40352825/714478
        pillow_image = Image.open(fifo_path)
        proc.wait()
        return pillow_image

    @contextmanager
    def _named_pipe(self, extension='bmp'):
        # Make a unique named pipe and return the path
        try:
            name = ''.join(choice(ascii_lowercase) for x in range(6))
            pth = '{0}.{1}'.format(join(self.tmp, name), extension)
            mkfifo(pth)
            yield pth
        finally:
            unlink(pth)

    @staticmethod
    def reduce_arg_from_image_request(image_request):
        req_w = image_request.width
        req_h = image_request.height
        full_w = image_request.info.width
        full_h = image_request.info.height
        scales = image_request.info.all_scales
        scales_to_reduce_arg = AbstractJp2Transcoder._scales_to_reduce_arg
        return scales_to_reduce_arg(req_w, req_h, full_w, full_h, scales)

    @staticmethod
    def _scales_to_reduce_arg(req_w, req_h, full_w, full_h, scales=[]):
        get_closest_scale = AbstractJp2Transcoder._get_closest_scale
        closest_scale = get_closest_scale(req_w, req_h, full_w, full_h, scales)
        reduce_arg = int(log(closest_scale, 2))
        return str(reduce_arg)

    @staticmethod
    def _scale_dimension(dim, scale):
        return ceil(dim/scale) # Kakadu and OpenJPEG always seem to ceil

    @staticmethod
    def _get_closest_scale(req_w, req_h, full_w, full_h, scales=[]):
        if (req_w > full_w or req_h > full_h) or not scales:
            return 1
        else:
            is_larger = AbstractJp2Transcoder._scale_is_larger
            larger_scales = [scale for scale in scales \
                if is_larger(req_w, req_h, full_w, full_h, scale)]
            return max(larger_scales)

    @staticmethod
    def _scale_is_larger(req_w, req_h, full_w, full_h, scale):
        # Returns True if scaling the full size image results in an image
        # that is larger than the request. The idea is to let the JP2 library
        # get us as close as possible to the image we want before PIL has to
        # take over.
        scale_dim = AbstractJp2Transcoder._scale_dimension
        w_larger = scale_dim(full_w, scale) >= req_w
        h_larger = scale_dim(full_h, scale) >= req_h
        return w_larger and h_larger
