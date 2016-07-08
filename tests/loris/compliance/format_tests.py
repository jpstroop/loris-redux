from loris.compliance.format import FormatCompliance

class TestFormatCompliance(object):
    def test_how_to_get_2(self):
        cfg = {
            'png': { 'enabled': True },
            'webp': { 'enabled': False }
        }
        assert FormatCompliance(cfg) == 2

    def test_format_is_1_without_png(self):
        cfg = {
            'png': { 'enabled': False },
            'webp': { 'enabled': True }
        }
        assert FormatCompliance(cfg) == 1

    def test_format_is_1_with_nothing(self):
        cfg = {
            'png': { 'enabled': False },
            'webp': { 'enabled': False }
        }
        assert FormatCompliance(cfg) == 1
