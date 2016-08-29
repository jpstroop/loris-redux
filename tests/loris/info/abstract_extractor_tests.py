from loris.info.abstract_extractor import AbstractExtractor
from loris.compliance import Compliance
from unittest.mock import Mock
import pytest

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

    def test_receives_compliance(self, app_configs):
        compliance = Mock(level=2)
        ex = ValidExtractor(compliance, app_configs)
        assert ex.compliance == compliance

    def test_max_size_area_only(self):
        max_area = 4000000
        w = 3000
        h = 2000
        size_entry = ValidExtractor.max_size(w, h, max_area=max_area)
        assert size_entry.width * size_entry.height < max_area
        assert size_entry.width == 2449
        assert size_entry.height == 1633

    def test_max_size_w_only(self):
        max_width = 2760
        w = 3000
        h = 2000
        size_entry = ValidExtractor.max_size(w, h, max_width=max_width)
        assert size_entry.width == 2760
        assert size_entry.height == 1840

    def test_max_size_h_only(self):
        max_height = 1000
        w = 3400
        h = 2254
        size_entry = ValidExtractor.max_size(w, h, max_height=max_height)
        assert size_entry.width == 1508
        assert size_entry.height == 1000

    def test_max_all_the_things(self):
        max_area = 4000000
        max_width = 1500
        max_height = 2700
        w = 6000
        h = 3798
        size_entry = ValidExtractor.max_size(w, h, max_area=max_area, max_width=max_width, max_height=max_height)
        assert size_entry.width == 1500
        assert size_entry.height == 950

    def test_max_none_set(self):
        w = 6000
        h = 3798
        size_entry = ValidExtractor.max_size(w, h)
        assert size_entry.width == w
        assert size_entry.height == h
