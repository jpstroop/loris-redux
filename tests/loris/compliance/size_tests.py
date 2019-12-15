from loris.compliance.size import SizeCompliance

class TestSizeCompliance(object):

    def test_2_plus(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': True },
            'sizeByWh': { 'enabled': True },
            'sizeUpscaling': { 'enabled': True },
        }
        assert SizeCompliance(cfg) == 2

    def test_1_wo_sizeByWh(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': False },
            'sizeByConfinedWh': { 'enabled': True },
            'sizeByWh': { 'enabled': False },
            'sizeUpscaling': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 1

    def test_1_wo_sizeByConfinedWh(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': False },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': True },
            'sizeUpscaling': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 1

    def test_how_to_get_1(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': False },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeUpscaling': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 1

    def test_0_wo_sizeByH(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': False },
            'sizeByPct': { 'enabled': False },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeUpscaling': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 0

    def test_0_wo_sizeByW(self):
        cfg = {
            'sizeByW': { 'enabled': False },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': False },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeUpscaling': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 0

    def test_how_to_get_2(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': True },
            'sizeByWh': { 'enabled': True },
            'sizeUpscaling': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 2

    def test_how_to_get_0(self):
        cfg = {
            'sizeByW': { 'enabled': False },
            'sizeByH': { 'enabled': False },
            'sizeByPct': { 'enabled': False },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeUpscaling': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 0
