from loris.compliance.http import HttpCompliance


class TestHttpCompliance(object):
    def test_how_to_get_2(self):
        cfg = {
            "baseUriRedirect": {"enabled": True},
            "cors": {"enabled": True},
            "jsonldMediaType": {"enabled": True},
            "profileLinkHeader": {"enabled": False},
            "canonicalLinkHeader": {"enabled": False},
        }
        assert HttpCompliance(cfg) == 2

    def test_0_wo_baseUriRedirect(self):
        cfg = {
            "baseUriRedirect": {"enabled": False},
            "cors": {"enabled": True},
            "jsonldMediaType": {"enabled": True},
            "profileLinkHeader": {"enabled": True},
            "canonicalLinkHeader": {"enabled": True},
        }
        assert HttpCompliance(cfg) == 0

    def test_0_wo_cors(self):
        cfg = {
            "baseUriRedirect": {"enabled": True},
            "cors": {"enabled": False},
            "jsonldMediaType": {"enabled": True},
            "profileLinkHeader": {"enabled": True},
            "canonicalLinkHeader": {"enabled": True},
        }
        assert HttpCompliance(cfg) == 0

    def test_2_with_everything(self):
        cfg = {
            "baseUriRedirect": {"enabled": True},
            "cors": {"enabled": True},
            "jsonldMediaType": {"enabled": True},
            "profileLinkHeader": {"enabled": True},
            "canonicalLinkHeader": {"enabled": True},
        }
        assert HttpCompliance(cfg) == 2
