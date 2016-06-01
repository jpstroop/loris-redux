import pytest
from os import path

HERE = path.abspath(path.dirname(__file__))
FIXTURES_DIR = path.join(HERE, 'fixtures')

@pytest.fixture()
def tiled_jp2():
    return path.join(FIXTURES_DIR, 'color.jp2')

@pytest.fixture()
def color_jpg():
    return path.join(FIXTURES_DIR, 'color.jpg')

@pytest.fixture()
def color_png():
    return path.join(FIXTURES_DIR, 'color.png')

@pytest.fixture()
def color_tif():
    return path.join(FIXTURES_DIR, 'color.tif')
