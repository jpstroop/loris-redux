from loris.info.abstract_extractor import AbstractExtractor
from loris.helpers.compliance import Compliance
from unittest.mock import Mock
import pytest

app_configs_wo_scale_factors = { 'scale_factors' : { 'enabled' : False } }

class ValidExtractor(AbstractExtractor):
    def __init__(self, compliance, app_configs):
        super().__init__(compliance, app_configs)

    def extract(path, http_identifier):
        return "doesn't matter here"

class TestAbstractExtractor(object):

    def test_extract_required(self):
        class WithoutExtract(AbstractExtractor):
            def foo(self):
                return 'bar'
        with pytest.raises(TypeError) as type_error:
            w = WithoutExtract('x')
        assert "Can't instantiate abstract class" in str(type_error.value)

    def test_receives_compliance_(self):
        compliance = Mock(level=2)
        ex = ValidExtractor(compliance, app_configs_wo_scale_factors)
        assert ex.compliance == compliance

    def test__level_zero_tiles_wide(self):
        tiles = AbstractExtractor._level_zero_tiles(7201, 3893, 1024, 1024)
        only_entry = tiles[0]
        assert only_entry['width'] == 1024
        assert only_entry.get('height') is None
        assert only_entry['scaleFactors'] == [1, 2, 4]

    def test__level_zero_tiles_tall(self):
        tiles = AbstractExtractor._level_zero_tiles(2000, 11003, 512, 512)
        only_entry = tiles[0]
        assert only_entry['width'] == 512
        assert only_entry.get('height') is None
        assert only_entry['scaleFactors'] == [1, 2, 4, 8, 16]

    # 7200 with tile size 1024 = 900, 450, 225, 114, 57
    def test__level_zero_sizes(self):
        sizes = AbstractExtractor._level_zero_sizes(4, 7201, 3664)
        assert sizes[0]['width'] == 901
        assert sizes[0]['height'] == 458
        assert sizes[1]['width'] == 451
        assert sizes[1]['height'] == 229
        assert sizes[2]['width'] == 226
        assert sizes[2]['height'] == 115
        assert sizes[3]['width'] == 113
        assert sizes[3]['height'] == 58
        assert sizes[4]['width'] == 57
        assert sizes[4]['height'] == 29
        assert sizes[5]['width'] == 29
        assert sizes[5]['height'] == 15
        assert sizes[6]['width'] == 15
        assert sizes[6]['height'] == 8
        assert sizes[7]['width'] == 8
        assert sizes[7]['height'] == 4
        assert sizes[8]['width'] == 4
        assert sizes[8]['height'] == 2
        assert sizes[9]['width'] == 2
        assert sizes[9]['height'] == 1
        with pytest.raises(IndexError):
            _ = sizes[10]

    def test_level_zero_tiles_and_sizes_raises(self):
        compliance = Mock(level=1)
        instance = ValidExtractor(compliance, app_configs_wo_scale_factors)
        with pytest.raises(Exception) as error:
            _ = instance.level_zero_tiles_and_sizes(400, 300, 100, 100)
        assert 'but server compliance is 1' in str(error.value)

    def test_max_size_area_only(self):
        max_area = 4000000
        w = 3000
        h = 2000
        size_entry = ValidExtractor.max_size(w, h, max_area=max_area)
        assert size_entry['width'] * size_entry['height'] < max_area
        assert size_entry['width'] == 2449
        assert size_entry['height'] == 1633

    def test_max_size_w_only(self):
        max_width = 2760
        w = 3000
        h = 2000
        size_entry = ValidExtractor.max_size(w, h, max_width=max_width)
        assert size_entry['width'] == 2760
        assert size_entry['height'] == 1840

    def test_max_size_h_only(self):
        max_height = 1000
        w = 3400
        h = 2254
        size_entry = ValidExtractor.max_size(w, h, max_height=max_height)
        assert size_entry['width'] == 1508
        assert size_entry['height'] == 1000

    def test_max_all_the_things(self):
        max_area = 4000000
        max_width = 1500
        max_height = 2700
        w = 6000
        h = 3798
        size_entry = ValidExtractor.max_size(w, h, max_area=max_area, max_width=max_width, max_height=max_height)
        assert size_entry['width'] == 1500
        assert size_entry['height'] == 950

    def test_max_none_set(self):
        w = 6000
        h = 3798
        size_entry = ValidExtractor.max_size(w, h)
        assert size_entry['width'] == w
        assert size_entry['height'] == h
