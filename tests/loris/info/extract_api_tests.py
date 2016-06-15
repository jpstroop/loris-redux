from loris.info.extract_api import AbstractExtractor
import pytest

class TestAbstractExtractor(object):

    def test_extract_required(self):
        class WithoutExtract(AbstractExtractor):
            def foo(self):
                return 'bar'
        with pytest.raises(TypeError) as type_error:
            w = WithoutExtract('x','y')
        assert "Can't instantiate abstract class" in str(type_error.value)

    def test_receives_compliance_and_base_uri(self):

        class ProperExtractor(AbstractExtractor):
            def extract(self,path, http_identifier):
                return 'bar'

        ex = ProperExtractor('compliance', 'base_uri')
        assert ex.compliance == 'compliance'
        assert ex.base_uri == 'base_uri'
