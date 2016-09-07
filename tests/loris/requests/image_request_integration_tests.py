from loris.requests.iiif_request import IIIFRequest
from loris.requests.image_request import ImageRequest

from datetime import datetime
from unittest.mock import patch

class TestImageRequest(object):
    # These tests integrate all the objects that do the heavy lifting around
    # checking supported features, determining the canoncal form of the params,
    # syntax checking, etc. It they are failing, check the imported classes
    # first!

    def test_canonical(self, compliance_2, tiled_jp2, app_configs):
        resolver_data = (tiled_jp2, 'jp2', 'no need for lastmod here')
        iiif_params = 'full/max/0/default.jpg'
        with patch.object(IIIFRequest, '_resolve_identifier', return_value=resolver_data):
            request = ImageRequest('fakeid', iiif_params)
            assert request.canonical == 'full/3622,/0/default.jpg'

    def test_etag(self, compliance_2, tiled_jp2, app_configs):
        lastmod = datetime(2016, 9, 4, 12, 28, 24, 928635)
        resolver_data = (tiled_jp2, 'jp2', lastmod)
        with patch.object(IIIFRequest, '_resolve_identifier', return_value=resolver_data):
        # etag could change if we update the test jp2 in any way, so instead
        # we're testing whether two equivalent requests yield the same etag
            request1 = ImageRequest('fakeid', 'full/max/0/default.jpg')
            request2 = ImageRequest('fakeid', 'full/3622,/0/default.jpg')
            assert request2.etag == request1.etag
