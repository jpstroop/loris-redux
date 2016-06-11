import pytest
import json
from os import path

HERE = path.abspath(path.dirname(__file__))
FIXTURES_DIR = path.join(HERE, 'fixtures')
COMPLIANCE_DIR = path.join(FIXTURES_DIR, 'compliance')

def _load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

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
