from loris.compliance.quality import QualityCompliance

class TestQualityCompliance(object):
    def test_how_to_get_2(self):
        cfg = {
            'color': { 'enabled': True },
            'gray': { 'enabled': True },
            'bitonal': { 'enabled': True }
        }
        assert QualityCompliance(cfg) == 2

    def test_1_with_nothing_enabled(self):
        cfg = {
            'color': { 'enabled': False },
            'gray': { 'enabled': False },
            'bitonal': { 'enabled': False }
        }
        assert QualityCompliance(cfg) == 1
