from loris.compliance.rotation import RotationCompliance


class TestRotationCompliance(object):
    def test_how_to_get_2(self):
        cfg = {
            "rotationBy90s": {"enabled": True},
            "rotationArbitrary": {"enabled": True},
            "mirroring": {"enabled": True},
        }
        assert RotationCompliance(cfg) == 2

    def test_1_with_nothing_enabled(self):
        cfg = {
            "rotationBy90s": {"enabled": False},
            "rotationArbitrary": {"enabled": False},
            "mirroring": {"enabled": False},
        }
        assert RotationCompliance(cfg) == 1
