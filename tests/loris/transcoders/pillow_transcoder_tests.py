from PIL import Image
from PIL.ImageOps import mirror
from io import BytesIO
from unittest.mock import Mock

import pytest

from loris.transcoders.pillow_transcoder import PillowTranscoder
from loris.constants import FULL
from loris.constants import REGION_BY_PIXEL

from tests.loris.transcoders.helpers import GREEN
from tests.loris.transcoders.helpers import RED
from tests.loris.transcoders.helpers import BLUE
from tests.loris.transcoders.helpers import ORANGE
from tests.loris.transcoders.helpers import PURPLE
from tests.loris.transcoders.helpers import DARK_SLATE
from tests.loris.transcoders.helpers import BLACK
from tests.loris.transcoders.helpers import WHITE

@pytest.fixture(scope='function')
def pillow_image(pillow_transcoder_test_bmp):
    return Image.open(pillow_transcoder_test_bmp)

@pytest.fixture(scope='module')
def transcoder():
    return PillowTranscoder({})

def parse_stream(stream):
    return Image.open(BytesIO(stream.getvalue()))

class TestPillowTranscoder(object):

    # Throughout these tests, use pillow_image.show() if you're confused

    def test__crop(self, transcoder, pillow_image):
        image_request = Mock(
            region_pixel_x = 200,
            region_pixel_y = 300,
            region_pixel_w = 200,
            region_pixel_h = 200
        )
        pillow_image = transcoder._crop(pillow_image, image_request)
        # Check the size, color of the top left corner pixels, and the four
        # center pixels.
        assert pillow_image.size == (200,200)
        with pytest.raises(IndexError) as ie:
            pillow_image.getpixel((0,200))
            pillow_image.getpixel((200,0))
        assert 'image index out of range' == str(ie.value)
        assert pillow_image.getpixel((0,0)) == DARK_SLATE # top left
        assert pillow_image.getpixel((99,99)) == GREEN
        assert pillow_image.getpixel((99,100)) == BLUE
        assert pillow_image.getpixel((100,99)) == RED
        assert pillow_image.getpixel((100,100)) == ORANGE

    def test__resize(self, transcoder, pillow_image):
        image_request = Mock(
            width = 349,
            height = 262
        )
        pillow_image = transcoder._resize(pillow_image, image_request)
        assert pillow_image.size == (349,262)

    def test__resize_will_distort_not_crop(self, transcoder, pillow_image):
        image_request = Mock(
            width = 349,
            height = 10
        )
        pillow_image = transcoder._resize(pillow_image, image_request)
        assert pillow_image.size == (349,10)
        assert pillow_image.getpixel((0,0)) == GREEN # top left
        assert pillow_image.getpixel((0,9)) == BLUE # bottom left

    def test_rotate_rotates_90(self, transcoder, pillow_image):
        # The behavior of expand is a little confusing. Make sure all pixels
        # rotate
        image_request = Mock(rotation=90)
        pillow_image = transcoder._rotate(pillow_image, image_request)
        assert pillow_image.size == (800,600)
        with pytest.raises(IndexError) as ie:
            pillow_image.getpixel((0,800))
            pillow_image.getpixel((600,0))
        assert 'image index out of range' == str(ie.value)
        assert pillow_image.getpixel((0,0)) == BLUE
        assert pillow_image.getpixel((399,299)) == BLUE
        assert pillow_image.getpixel((400,299)) == GREEN
        assert pillow_image.getpixel((399,300)) == ORANGE
        assert pillow_image.getpixel((400,300)) == RED

    def test_mirror(self, transcoder, pillow_image):
        pillow_image = mirror(pillow_image)
        assert pillow_image.getpixel((299,399)) == RED
        assert pillow_image.getpixel((300,399)) == GREEN
        assert pillow_image.getpixel((299,400)) == ORANGE
        assert pillow_image.getpixel((300,400)) == BLUE

    def test_rotate_non_90_expands(self, transcoder, pillow_image):
        image_request = Mock(rotation=135)
        pillow_image = transcoder._rotate(pillow_image, image_request)
        assert pillow_image.size == (991,990)

    def test_rotate_non_90_png_has_transparent_alpha(self, transcoder, pillow_image):
        # TODO: need a similar test for saved images
        image_request = Mock(rotation=235, format='png')
        pillow_image = transcoder._rotate(pillow_image, image_request)
        r, g, b, a = pillow_image.getpixel((0,0))
        assert a == 0

    def test_default_quality(self, transcoder, pillow_image):
        image_request = Mock(quality='default')
        pillow_image = transcoder._adjust_quality(pillow_image, image_request)
        assert pillow_image.mode == 'RGB'

    def test_bitonal_quality(self, transcoder, pillow_image):
        image_request = Mock(quality='bitonal')
        pillow_image = transcoder._adjust_quality(pillow_image, image_request)
        assert pillow_image.mode == '1'

    def test_gray_quality(self, transcoder, pillow_image):
        image_request = Mock(quality='gray')
        pillow_image = transcoder._adjust_quality(pillow_image, image_request)
        assert pillow_image.mode == 'L'

    def test_color_quality(self, transcoder, pillow_image):
        image_request = Mock(quality='color')
        pillow_image = transcoder._adjust_quality(pillow_image, image_request)
        assert pillow_image.mode == 'RGB'

    def test_rotated_color_transparency(self, transcoder, pillow_image):
        # We need to integrate all of the methods to make sure we're saving the
        # correct mode
        image_request = Mock(
            region_request_type=FULL,
            size_request_type=FULL,
            rotation=95,
            quality='color',
            format='png'
        )
        stream = transcoder.execute_with_pil_image(pillow_image, image_request)
        pillow_image = parse_stream(stream)
        assert pillow_image.mode == 'RGBA'
        assert pillow_image.getpixel((0,0))[-1] == 0

    def test_rotated_default_transparency(self, transcoder, pillow_image):
        image_request = Mock(
            region_request_type=FULL,
            size_request_type=FULL,
            rotation=95,
            quality='default',
            format='png'
        )
        stream = transcoder.execute_with_pil_image(pillow_image, image_request)
        pillow_image = parse_stream(stream)
        assert pillow_image.mode == 'RGBA'
        assert pillow_image.getpixel((0,0))[-1] == 0

    def test_rotated_gray_transparency(self, transcoder, pillow_image):
        image_request = Mock(
            region_request_type=FULL,
            size_request_type=FULL,
            rotation=95,
            quality='gray',
            format='png'
        )
        stream = transcoder.execute_with_pil_image(pillow_image, image_request)
        pillow_image = parse_stream(stream)
        assert pillow_image.mode == 'LA'
        assert pillow_image.getpixel((0,0))[-1] == 0

    def test_crop(self, transcoder, pillow_image):
        image_request = Mock(
            region_request_type = REGION_BY_PIXEL,
            region_pixel_x = 100,
            region_pixel_y = 200,
            region_pixel_w = 300,
            region_pixel_h = 400,
            size_request_type=FULL,
            width = 300,
            height = 400,
            rotation=0,
            quality='gray',
            format='png'
        )
        stream = transcoder.execute_with_pil_image(pillow_image, image_request, crop=True)
        pillow_image = parse_stream(stream)
        assert pillow_image.size == (300,400)
        # TODO: might want to check pixels

    def test_execute(self, transcoder, region_test_jpg):
        image_request = Mock(
            file_path = region_test_jpg,
            region_request_type = FULL,
            region_pixel_x = 0,
            region_pixel_y = 0,
            region_pixel_w = 6000,
            region_pixel_h = 8000,
            size_request_type=FULL,
            width = 6000,
            height = 8000,
            mirror = False,
            rotation = 0.0,
            quality = 'default',
            format='jpg'
        )
        stream = transcoder.execute(image_request)
        pillow_image = parse_stream(stream)
        assert pillow_image.size == (6000,8000)

    image_formats = (
        ('png', 'PNG'),
        ('jpg', 'JPEG'),
        ('webp', 'WEBP'),
        ('gif', 'GIF')
    )
    @pytest.fixture(scope='module', params=image_formats)
    def fmt(self, request):
        yield request.param

    def test_output_formats(self, transcoder, pillow_image, fmt):
        image_request = Mock(
            region_request_type=FULL,
            size_request_type=FULL,
            rotation=0,
            quality='default',
            format=fmt[0]
        )
        stream = transcoder.execute_with_pil_image(pillow_image, image_request)
        pillow_image = parse_stream(stream)
        assert pillow_image.format == fmt[1]
