from PIL import Image
from PIL.ImageFile import Parser
from PIL.ImageOps import mirror
from logging import getLogger

logger = getLogger('loris')

class PillowDerviativeMixin(object):

    def execute(self, image_request):
        im = Image.open(image_request.file_path)
        return self.execute_with_pil_image(image_request, im)

    def execute_with_pil_image(self, image_request, pil_image):
        pass
    # # This is left out of the abstract class in case there is ever a desire
    # # to write a Transcoder that encodes w/ another library, e.g. VIPS.
    #
    # # TODO: move and refactor code from Loris. The idea is that, e.g. any
    # # Transcoder could subclass loris.transcoders.api.AbstractTranscoder
    # # and this.
    # # TODO: test coverage
    # # not caching.
    # # See: http://pillow.readthedocs.io/en/latest/reference/Image.html#PIL.Image.Image.tobytes
    # # and: http://pillow.readthedocs.io/en/latest/reference/Image.html#PIL.Image.Image.save
    # def derive(self, pil_im, image_request, rotate=True, crop=True):
    #     '''
    #     Once you have a PIL.Image, this can be used to do the IIIF operations.
    #
    #     Args:
    #         im (PIL.Image)
    #         target_fp (str)
    #         image_request (ImageRequest)
    #         rotate (bool):
    #             True by default; can be set to False in case the rotation was
    #             done further upstream.
    #         crop (bool):
    #             True by default; can be set to False when the region was aleady
    #             extracted further upstream.
    #     Returns:
    #         void (puts an image at target_fp)
    #
    #     '''
    #     self.dither_bitonal_images = self.config.get('dither_bitonal_images', True)
    #
    #     pass
