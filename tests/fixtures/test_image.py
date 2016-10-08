#!/usr/bin/env python

# Draw a fixture image with known features that we can use in tests.

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import unittest

IMAGE_WIDTH = 6000
IMAGE_HEIGHT = 8000


GREEN = (0, 150, 0)
RED = (150, 0, 0)
BLUE = (0, 0, 150)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
DARK_SLATE = (49, 79, 79)
BLACK = (0 ,0 ,0)
WHITE = (255 ,255 ,255)

# /usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf
FONT = ImageFont.truetype('DejaVuSansMono.ttf', 120)

def create_image():
    # start with a black image
    image = Image.new(mode='RGB', size=(IMAGE_WIDTH, IMAGE_HEIGHT))
    draw = ImageDraw.Draw(image)

    # TOP LEFT QUADRANT
    draw.rectangle((0, 0, 2999, 3999), fill=GREEN)
    draw.text((200, 200), '0,0,3000,4000', font=FONT, fill=BLACK)

    # TOP_RIGHT_QUADRANT
    draw.rectangle((3000, 0, 5999, 3999), fill=RED)
    draw.text((3200, 200), '3000,0,3000,4000', font=FONT, fill=BLACK)

    # BOTTOM_LEFT_QUADRANT
    draw.rectangle((0, 4000, 2999, 7999), fill=BLUE)
    draw.text((200, 4600), '0,4000,3000,4000', font=FONT, fill=WHITE)

    # BOTTOM_RIGHT_QUADRANT
    draw.rectangle((3000, 4000, 5999, 7999), fill=ORANGE)
    draw.text((3200, 4200), '3000,4000,3000,4000', font=FONT, fill=BLACK)

    # RANDOM_RECTANGLE_1
    draw.rectangle((2000, 5000, 4999, 6999), fill=PURPLE)
    draw.text((2200, 5200), '2000,5000,3000,2000', font=FONT, fill=BLACK)

    # RANDOM_RECTANGLE_2
    draw.rectangle((1000, 1500, 2499, 4499), fill=DARK_SLATE)
    draw.text((1050,1700), '1000,1500,1500,3000', font=FONT, fill=BLACK)

    return image

class TestImageFeatures(unittest.TestCase):
    def setUp(self):
        self.image = create_image()
    def test_size(self):
        self.assertEqual(self.image.size, (6000, 8000))
        with self.assertRaises(IndexError):
            self.image.getpixel((6000, 8000)) # because zero based...
    def test_top_left_top_left(self):
        self.assertEqual(self.image.getpixel((0, 0)), GREEN)
    def test_top_left_top_right(self):
        self.assertEqual(self.image.getpixel((2999, 0)), GREEN)
    def test_top_left_bottom_left(self):
        self.assertEqual(self.image.getpixel((0, 3999)), GREEN)
    def test_top_left_bottom_right(self):
        self.assertEqual(self.image.getpixel((2999, 3999)), GREEN)
    def test_top_right_top_left(self):
        self.assertEqual(self.image.getpixel((3000, 0)), RED)
    def test_top_right_top_right(self):
        self.assertEqual(self.image.getpixel((5999, 0)), RED)
    def test_top_right_bottom_left(self):
        self.assertEqual(self.image.getpixel((3090, 3999)), RED)
    def test_top_right_bottom_right(self):
        self.assertEqual(self.image.getpixel((5999, 3999)), RED)
    def test_bottom_left_top_left(self):
        self.assertEqual(self.image.getpixel((0, 4000)), BLUE)
    def test_bottom_left_top_right(self):
        self.assertEqual(self.image.getpixel((2999, 4000)), BLUE)
    def test_bottom_left_bottom_left(self):
        self.assertEqual(self.image.getpixel((0, 7999)), BLUE)
    def test_bottom_left_bottom_right(self):
        self.assertEqual(self.image.getpixel((2999, 7999)), BLUE)
    def test_bottom_right_top_left(self):
        self.assertEqual(self.image.getpixel((3000, 4000)), ORANGE)
    def test_bottom_right_top_right(self):
        self.assertEqual(self.image.getpixel((5999, 4000)), ORANGE)
    def test_bottom_right_bottom_left(self):
        self.assertEqual(self.image.getpixel((3000, 7999)), ORANGE)
    def test_bottom_right_bottom_right(self):
        self.assertEqual(self.image.getpixel((5999, 7999)), ORANGE)



if __name__ == '__main__':
    # unittest.main() # uncomment to run the tests. They aren't run as part
                      # of the suite right now. Probably should be.
    create_image().show(command='/usr/bin/eog')
    # create_image().save('region_test.jpg')
    # create_image().save('region_test.tif')

    # kdu_compress -i region_test.tif -o region_test.jp2 -rate 2.4,1.48331273,.91673033,.56657224,.35016049,.21641118,.13374944,.08266171 Creversible=yes Clevels=7 Cblk=\{64,64\} -jp2_space sRGB Cuse_sop=yes Cuse_eph=yes Corder=RLCP ORGgen_plt=yes ORGtparts=R Stiles=\{1024,1024\} -double_buffering 10 -no_weights
