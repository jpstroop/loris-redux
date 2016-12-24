from io import BytesIO
from logging import getLogger
from math import ceil
from PIL import Image
from PIL.ImageOps import mirror

from loris.constants import FULL
from loris.transcoders.api import AbstractTranscoder

logger = getLogger('loris')

class PillowTranscoder(object):

    def __init__(self, config={}): # pylint:disable=dangerous-default-value
        AbstractTranscoder.__init__(self, config)

    def execute(self, image_request):
        # This covers the API and can be used for non-Jp2s. The real work
        # is in #execute_with_pil_image (below), which takes a 3rd param,
        # a PIL.Image, which the Jp2Transcoders can hand off to this transcoder
        # for further processing and ulitmate encoding.
        pil_image = Image.open(image_request.file_path)
        return self.execute_with_pil_image(pil_image, image_request, crop=True)

    def execute_with_pil_image(self, pil_image, image_request, crop=False, dither=Image.FLOYDSTEINBERG):
        if crop and image_request.region_request_type is not FULL:
            pil_image = self._crop(pil_image, image_request)
        if image_request.size_request_type is not FULL:
            pil_image = self._resize(pil_image, image_request)
        if image_request.mirror:
            pil_image = mirror(pil_image)
        if image_request.rotation != 0.0:
            pil_image = self._rotate(pil_image, image_request)
        if image_request.quality != 'default':
            pil_image = self._adjust_quality(pil_image, image_request, dither=dither)
        return self._save_to_bytesio(pil_image, image_request)

    def _crop(self, pil_image, image_request):
        pil_box = ( # it's really that expensive kind ♫
            image_request.region_pixel_x,
            image_request.region_pixel_y,
            image_request.region_pixel_x + image_request.region_pixel_w,
            image_request.region_pixel_y + image_request.region_pixel_h
        )
        return pil_image.crop(pil_box)

    def _resize(self, pil_image, image_request, sampling=Image.LANCZOS):
        wh = (image_request.width, image_request.height)
        pil_image = pil_image.resize(wh, resample=sampling)
        return pil_image

    def _rotate(self, pil_image, image_request):
        rotation = 0 - image_request.rotation # PIL goes counter-clockwise
        expand = bool(rotation) # i.e. if not 0
        if expand and image_request.format == 'png':
            # We need to convert to add an alpha channel so that we get q
            # transparent background:
            if image_request.quality in ('gray', 'bitonal'):
                pil_image = pil_image.convert('LA')
            else:
                pil_image = pil_image.convert('RGBA')
        return pil_image.rotate(rotation, expand=expand)

    def _adjust_quality(self, pil_image, image_request, dither=Image.FLOYDSTEINBERG):
        # See: http://pillow.readthedocs.io/en/3.3.x/handbook/concepts.html#concept-modes
        if pil_image.mode in ('RGBA', 'LA'):
            return pil_image # this probably happened upstream during rotation
        elif pil_image.mode != 'RGB' and image_request.quality not in ('gray', 'bitonal'):
            return pil_image.convert('RGB')
        elif image_request.quality == 'gray':
            return pil_image.convert('L')
        elif image_request.quality == 'bitonal':
            return pil_image.convert('1', dither=dither)
        return pil_image

    def _save_to_bytesio(self, pil_image, image_request):
        stream = BytesIO()
        if image_request.format == 'jpg':
            # see http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#jpeg
            pil_image.save(stream, quality=90, format='jpeg')
        elif image_request.format == 'png':
            # see http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#png
            pil_image.save(stream, optimize=True, bits=256, format='png')
        elif image_request.format == 'gif':
            # see http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#gif
            pil_image.save(stream, format='gif')
        elif image_request.format == 'webp':
            # see http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html#webp
            pil_image.save(stream, quality=90, format='webp')
        return stream
