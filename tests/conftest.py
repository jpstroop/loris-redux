from loris.compliance import Compliance
from loris.helpers.safe_lru_dict import SafeLruDict
from loris.info.jp2_extractor import Jp2Extractor
from loris.loris_app import cherrypy_app_conf
from loris.loris_app import LorisApp
from loris.requests.iiif_request import IIIFRequest
from os import path
from os import remove
from tests.loris.handlers.base_handler_test import SOCKET_HOST
from tests.loris.handlers.base_handler_test import SOCKET_PORT
from warnings import simplefilter
import cherrypy
import pytest
import yaml

HERE = path.abspath(path.dirname(__file__))
FIXTURES_DIR = path.join(HERE, 'fixtures')
IMAGES_DIR = path.join(FIXTURES_DIR, 'images')
COMPLIANCE_DIR = path.join(FIXTURES_DIR, 'compliance')

LORIS_CONFIG_FILE = path.join(HERE, '../loris/config.yaml')
COLOR_JP2 = path.join(IMAGES_DIR, 'color.jp2')
GRAY_JP2 = path.join(IMAGES_DIR, 'gray.jp2')
COLOR_PROFILE_JP2 = path.join(IMAGES_DIR, 'weird_color_profile.jp2')
PRECINCTS_JP2 = path.join(IMAGES_DIR, 'precincts.jp2')
COLOR_JPG = path.join(IMAGES_DIR, 'color.jpg')
COLOR_PNG = path.join(IMAGES_DIR, 'color.png')
COLOR_TIF = path.join(IMAGES_DIR, 'color.tif')
GRAY_JPG = path.join(IMAGES_DIR, 'gray.jpg')
GRAY_PNG = path.join(IMAGES_DIR, 'gray.png')
GRAY_TIF = path.join(IMAGES_DIR, 'gray.tif')
REGION_TEST_JPG = path.join(IMAGES_DIR, 'region_test.jpg')
REGION_TEST_JP2 = path.join(IMAGES_DIR, 'region_test.jp2')
PILLOW_TRANSCODER_TESTS_BMP = path.join(IMAGES_DIR, 'pillow_transcoder_tests.bmp')
TEST_IMAGES = ( COLOR_JP2, GRAY_JP2, COLOR_PROFILE_JP2, PRECINCTS_JP2,
    COLOR_JPG, COLOR_PNG, COLOR_TIF, GRAY_JPG, GRAY_PNG, GRAY_TIF,
    PILLOW_TRANSCODER_TESTS_BMP )

IMAGES_URL = 'http://www.princeton.edu/~jstroop/loris_test_images/images.tgz'

simplefilter('ignore', ResourceWarning)

def _download(url, to_dir):
    import requests
    local_filename = path.join(to_dir, url.split('/')[-1])
    r = requests.get(url)
    r.raise_for_status()
    with open(local_filename, 'wb') as f:
        f.write(r.content)
    return local_filename

def _load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session", autouse=True)
def download_images():
    # Fight repo bloat by keeping test images out.
    if not all([path.exists(p) for p in TEST_IMAGES]):
        import tarfile
        print('\n'+'*'*80)
        print('Downloading Test Images from \n{0}'.format(IMAGES_URL))
        print('*'*80)
        images_tarball = _download(IMAGES_URL, IMAGES_DIR)
        with tarfile.open(images_tarball, 'r:') as tar:
            tar.extractall(path=IMAGES_DIR)
        remove(images_tarball)

@pytest.fixture(scope="session", autouse=True)
def app_server():
    """Test server for handler tests
    """
    _configure_test_server()
    cherrypy.engine.start()
    cherrypy.engine.wait(cherrypy.engine.states.STARTED)
    yield
    cherrypy.engine.exit()
    cherrypy.engine.block()

def _configure_test_server():
    server_conf = {
        "server.socket_port": SOCKET_PORT,
        "server.socket_host": SOCKET_HOST,
    }
    cherrypy.config.update(server_conf)
    cherrypy.tree.mount(LorisApp(), "/", config=cherrypy_app_conf)

@pytest.fixture(scope='function')
def default_configs():
    # wish we didn't have to load this from disk every time, but it seems like
    # the only way to have it reset
    return _load_yaml(LORIS_CONFIG_FILE)

@pytest.fixture(scope='function')
def app_configs(default_configs):
    return default_configs['application']

@pytest.fixture(scope='function')
def fixtures_dir(default_configs):
    return FIXTURES_DIR

@pytest.fixture(scope='session')
def tiled_jp2():
    return COLOR_JP2

@pytest.fixture(scope='session')
def gray_jp2():
    return GRAY_JP2

@pytest.fixture(scope='session')
def color_profile_jp2():
    return COLOR_PROFILE_JP2

@pytest.fixture(scope='session')
def precincts_jp2():
    return PRECINCTS_JP2

@pytest.fixture(scope='session')
def region_test_jp2():
    return REGION_TEST_JP2

@pytest.fixture(scope='session')
def color_jpg():
    return COLOR_JPG

@pytest.fixture(scope='session')
def region_test_jpg():
    return REGION_TEST_JPG

@pytest.fixture(scope='session')
def pillow_transcoder_test_bmp():
    return PILLOW_TRANSCODER_TESTS_BMP

@pytest.fixture(scope='session')
def color_png():
    return COLOR_PNG

@pytest.fixture(scope='session')
def color_tif():
    return COLOR_TIF

@pytest.fixture(scope='session')
def gray_jpg():
    return GRAY_JPG

@pytest.fixture(scope='session')
def gray_png():
    return GRAY_PNG

@pytest.fixture(scope='session')
def gray_tif():
    return GRAY_TIF

# JSON fixtures for features

@pytest.fixture(scope='session')
def level0_scales_enabled_yaml():
    pth = path.join(COMPLIANCE_DIR, 'level0_scales_enabled.yaml')
    return _load_yaml(pth)

@pytest.fixture(scope='session')
def level1_exactly_yaml():
    pth = path.join(COMPLIANCE_DIR, 'level1_exactly.yaml')
    return _load_yaml(pth)

@pytest.fixture(scope='session')
def everything_enabled_yaml():
    pth = path.join(COMPLIANCE_DIR, 'everything_enabled.yaml')
    return _load_yaml(pth)

@pytest.fixture(scope='session')
def level0_plus_sizeByW_yaml():
    pth = path.join(COMPLIANCE_DIR, 'level0_plus_sizeByW.yaml')
    return _load_yaml(pth)

@pytest.fixture(scope='session')
def level1_plus_sizeByConfinedWh_yaml():
    pth = path.join(COMPLIANCE_DIR, 'level1_plus_sizeByConfinedWh.yaml')
    return _load_yaml(pth)

@pytest.fixture(scope='session')
def level2_plus_yaml():
    pth = path.join(COMPLIANCE_DIR, 'level2_plus.yaml')
    return _load_yaml(pth)

@pytest.fixture(scope='session')
def everything_but_regionByPx_yaml():
    pth = path.join(COMPLIANCE_DIR, 'everything_but_regionByPx.yaml')
    return _load_yaml(pth)

@pytest.fixture(scope='session')
def everything_but_sizeByConfinedWh_yaml():
    pth = path.join(COMPLIANCE_DIR, 'everything_but_sizeByConfinedWh.yaml')
    return _load_yaml(pth)

@pytest.fixture(scope='session')
def level0_nothing_yaml():
    pth = path.join(COMPLIANCE_DIR, 'level0.yaml')
    return _load_yaml(pth)

# Compliance Fixtures

@pytest.fixture()
def compliance_2(everything_enabled_yaml):
    return Compliance(everything_enabled_yaml)

@pytest.fixture()
def compliance_1(level1_exactly_yaml):
    return Compliance(level1_exactly_yaml)

@pytest.fixture()
def compliance_0(level0_nothing_yaml):
    return Compliance(level0_nothing_yaml)

# Sets up IIIFRequest as the application would have it.
@pytest.fixture(autouse=True, scope='function')
def set_up_iiif_request(app_configs, compliance_2):
    IIIFRequest.app_configs = app_configs
    IIIFRequest.extractors = {
        'jp2' : Jp2Extractor(compliance_2, app_configs)
    }
    IIIFRequest.info_cache = SafeLruDict()
    IIIFRequest.compliance = compliance_2
