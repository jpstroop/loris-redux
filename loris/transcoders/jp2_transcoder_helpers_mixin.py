from math import ceil
from math import log
from os import makedirs
from os import mkfifo
from os.path import join
from random import choice
from string import ascii_lowercase

class Jp2TranscoderHelpersMixin(object):
    # Any code that can be shared between the OpenJpegJp2Transcoder and the
    # KakaduJp2Transcoder goes here.
    def __init__(self, config):
        self.tmp = config.get('tmp', '/tmp/loris_tmp')
        makedirs(self.tmp, exist_ok=True) # let errors bubble up for now
        self.lib = None
        self.bin = None
        self.env = {
            'LD_LIBRARY_PATH' : self.lib,
            'PATH' : self.bin
        }

    def make_named_pipe(self, extension='bmp'):
        # Make a unique named pipe and return the path
        name = ''.join(choice(ascii_lowercase) for x in range(5))
        pth = '{0}.{1}'.format(join(self.tmp, name), extension)
        mkfifo(pth)
        return pth

    @staticmethod
    def execute_shellout(cmd, image_request):
        pass
        # TODO: use run: https://docs.python.org/3/library/subprocess.html#subprocess.run
        # TODO: do the shellout, finish deriving w/ PIL, return bytes or whatev.


    @staticmethod
    def reduce_arg_from_image_request(image_request):
        req_w = image_request.width
        req_h = image_request.height
        full_w = image_request.info.width
        full_h = image_request.info.height
        scales = image_request.info.all_scales
        scales_to_reduce_arg = Jp2TranscoderHelpersMixin._scales_to_reduce_arg
        return scales_to_reduce_arg(req_w, req_h, full_w, full_h, scales)

    @staticmethod
    def _scales_to_reduce_arg(req_w, req_h, full_w, full_h, scales=[]):
        get_closest_scale = Jp2TranscoderHelpersMixin._get_closest_scale
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
            is_larger = Jp2TranscoderHelpersMixin._scale_is_larger
            larger_scales = [scale for scale in scales \
                if is_larger(req_w, req_h, full_w, full_h, scale)]
            return max(larger_scales)

    @staticmethod
    def _scale_is_larger(req_w, req_h, full_w, full_h, scale):
        # Returns True if scaling the full size image results in an image
        # that is larger than the request. The idea is to let the JP2 library
        # get us as close as possible to the image we want before PIL has to
        # take over.
        scale_dim = Jp2TranscoderHelpersMixin._scale_dimension
        w_larger = scale_dim(full_w, scale) >= req_w
        h_larger = scale_dim(full_h, scale) >= req_h
        return w_larger and h_larger
