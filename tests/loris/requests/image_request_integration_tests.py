from loris.requests.image_request import ImageRequest
from loris.info.jp2_extractor import Jp2Extractor
import pytest

HTTP_ID = 'https://example.edu/no/matter'

class TestImageRequest(object):
    # These tests integrate all the objects that do the heavy lifting around
    # checking supported features, determining the canoncal form of the params,
    # syntax checking, etc. It they are failing, check everything else first!

    def stage_request(self, iiif_params, compliance_2, tiled_jp2, app_configs):
        extractor = Jp2Extractor(compliance_2, app_configs)
        info = extractor.extract(tiled_jp2, HTTP_ID)
        return ImageRequest(tiled_jp2, iiif_params, compliance_2, info)


    def test_canonical(self, compliance_2, tiled_jp2, app_configs):
        # fixtures (method args above) are in conftest.py
        iiif_params = 'full/max/0/default.jpg'
        request = self.stage_request(iiif_params, compliance_2, tiled_jp2, app_configs)
        assert request.canonical == 'full/3622,/0/default.jpg'

    def test_etag(self, compliance_2, tiled_jp2, app_configs):
        # Warning: etag could change if we update the test jp2 in any way, so
        # instead we're testing whether two equivalent requests yield the same
        # etag
        params1 = 'full/max/0/default.jpg'
        request1 = self.stage_request(params1, compliance_2, tiled_jp2, app_configs)
        params2 = 'full/3622,/0/default.jpg'
        request2 = self.stage_request(params2, compliance_2, tiled_jp2, app_configs)
        assert request2.etag == request1.etag
