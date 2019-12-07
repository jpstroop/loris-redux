from loris.compliance.region import RegionCompliance

class TestRegionCompliance(object):
    def test_how_to_get_2(self):
        cfg = {
            'regionByPx': { 'enabled': True },
            'regionByPct': { 'enabled': True },
            'regionSquare': { 'enabled': True }
        }
        assert RegionCompliance(cfg) == 2

    def test_how_to_get_1(self):
        cfg = {
            'regionByPx': { 'enabled': True },
            'regionByPct': { 'enabled': False },
            'regionSquare': { 'enabled': True }
        }
        assert RegionCompliance(cfg) == 1

    def test_how_to_get_0(self):
        cfg = {
            'regionByPx': { 'enabled': False },
            'regionByPct': { 'enabled': False },
            'regionSquare': { 'enabled': False }
        }
        assert RegionCompliance(cfg) == 0

    def test_how_to_get_2(self):
        cfg = {
            'regionByPx': { 'enabled': True },
            'regionByPct': { 'enabled': True },
            'regionSquare': { 'enabled': True }
        }
        assert RegionCompliance(cfg) == 2

    def test_still_0_with_addl(self):
        cfg = {
            'regionByPx': { 'enabled': False },
            'regionByPct': { 'enabled': False },
            'regionSquare': { 'enabled': True }
        }
        assert RegionCompliance(cfg) == 0
