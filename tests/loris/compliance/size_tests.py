from loris.compliance.size import SizeCompliance

class TestSizeCompliance(object):

    def test_2_plus(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': True },
            'sizeByDistortedWh': { 'enabled': True },
            'sizeByWh': { 'enabled': True },
            'sizeAboveFull': { 'enabled': True },
        }
        assert SizeCompliance(cfg) == 2

    def test_1_wo_sizeByWh(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': True },
            'sizeByDistortedWh': { 'enabled': True },
            'sizeByWh': { 'enabled': False },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 1

    def test_1_wo_sizeByDistortedWh(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': True },
            'sizeByDistortedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': True },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 1

    def test_1_wo_sizeByConfinedWh(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByDistortedWh': { 'enabled': True },
            'sizeByWh': { 'enabled': True },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 1

    def test_how_to_get_1(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByDistortedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 1

    def test_0_wo_sizeByPct(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': False },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByDistortedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 0

    def test_0_wo_sizeByH(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': False },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByDistortedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 0

    def test_0_wo_sizeByW(self):
        cfg = {
            'sizeByW': { 'enabled': False },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByDistortedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 0

    def test_how_to_get_2(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': True },
            'sizeByPct': { 'enabled': True },
            'sizeByConfinedWh': { 'enabled': True },
            'sizeByDistortedWh': { 'enabled': True },
            'sizeByWh': { 'enabled': True },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 2

    def test_how_to_get_0(self):
        cfg = {
            'sizeByW': { 'enabled': True },
            'sizeByH': { 'enabled': False },
            'sizeByPct': { 'enabled': False },
            'sizeByConfinedWh': { 'enabled': False },
            'sizeByDistortedWh': { 'enabled': False },
            'sizeByWh': { 'enabled': False },
            'sizeAboveFull': { 'enabled': False },
        }
        assert SizeCompliance(cfg) == 0
