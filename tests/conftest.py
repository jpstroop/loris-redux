from os import path
from os import remove
import json
import pytest

HERE = path.abspath(path.dirname(__file__))
FIXTURES_DIR = path.join(HERE, 'fixtures')
IMAGES_DIR = path.join(FIXTURES_DIR, 'images')
COMPLIANCE_DIR = path.join(FIXTURES_DIR, 'compliance')

COLOR_JP2 = path.join(IMAGES_DIR, 'color.jp2')
COLOR_JPG = path.join(IMAGES_DIR, 'color.jpg')
COLOR_PNG = path.join(IMAGES_DIR, 'color.png')
COLOR_TIF = path.join(IMAGES_DIR, 'color.tif')
GRAY_JPG = path.join(IMAGES_DIR, 'gray.jpg')
GRAY_PNG = path.join(IMAGES_DIR, 'gray.png')
GRAY_TIF = path.join(IMAGES_DIR, 'gray.tif')
TEST_IMAGES = ( COLOR_JP2, COLOR_JPG, COLOR_PNG, COLOR_TIF, GRAY_JPG, GRAY_PNG, GRAY_TIF )

IMAGES_URL = 'http://www.princeton.edu/~jstroop/loris_test_images/images.tar'

def _download(url, to_dir):
    import requests
    local_filename = path.join(to_dir, url.split('/')[-1])
    r = requests.get(url)
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
        f.write(r.content)
    return local_filename

def _load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

@pytest.fixture(scope="session", autouse=True)
def download_images():
    # Fight repo bloat by keeping test images out.
    if not all([path.exists(p) for p in TEST_IMAGES]):
        import tarfile
        print('\n'+'*'*80)
        print('Downloading Test Images from {0}'.format(IMAGES_URL))
        print('*'*80)
        images_tarball = _download(IMAGES_URL, IMAGES_DIR)
        with tarfile.open(images_tarball, 'r:') as tar:
            tar.extractall(path=IMAGES_DIR)
        remove(images_tarball)

@pytest.fixture()
def tiled_jp2():
    return COLOR_JP2

@pytest.fixture()
def color_jpg():
    return COLOR_JPG

@pytest.fixture()
def color_png():
    return COLOR_PNG

@pytest.fixture()
def color_tif():
    return COLOR_TIF

@pytest.fixture()
def gray_jpg():
    return GRAY_JPG

@pytest.fixture()
def gray_png():
    return GRAY_PNG

@pytest.fixture()
def gray_tif():
    return GRAY_TIF

@pytest.fixture()
def level0_scales_enabled_json():
    pth = path.join(COMPLIANCE_DIR, 'level0_scales_enabled.json')
    return _load_json(pth)

@pytest.fixture()
def level1_exactly_scales_enabled_json():
    pth = path.join(COMPLIANCE_DIR, 'level1_exactly_scales_enabled.json')
    return _load_json(pth)

@pytest.fixture()
def everything_enabled_json():
    pth = path.join(COMPLIANCE_DIR, 'everything_enabled.json')
    return _load_json(pth)

@pytest.fixture()
def level0_plus_sizeByW_json():
    pth = path.join(COMPLIANCE_DIR, 'level0_plus_sizeByW.json')
    return _load_json(pth)

@pytest.fixture()
def level1_plus_sizeByConfinedWh_json():
    pth = path.join(COMPLIANCE_DIR, 'level1_plus_sizeByConfinedWh.json')
    return _load_json(pth)

@pytest.fixture()
def level2_plus_json():
    pth = path.join(COMPLIANCE_DIR, 'level2_plus.json')
    return _load_json(pth)

@pytest.fixture()
def everything_but_regionByPx_json():
    pth = path.join(COMPLIANCE_DIR, 'everything_but_regionByPx.json')
    return _load_json(pth)

@pytest.fixture()
def everything_but_sizeByConfinedWh_json():
    pth = path.join(COMPLIANCE_DIR, 'everything_but_sizeByConfinedWh.json')
    return _load_json(pth)
