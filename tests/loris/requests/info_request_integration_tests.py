from loris.requests.iiif_request import IIIFRequest
from loris.requests.info_request import InfoRequest

from datetime import datetime
from unittest.mock import patch

class TestInfoRequest(object):
    # These tests integrate all the objects that do the heavy lifting around
    # checking supported features, determining the canoncal form of the params,
    # syntax checking, etc. It they are failing, check the imported classes
    # first!

    def test_etag(self, compliance_2, tiled_jp2, app_configs):
        lastmod = datetime(2016, 9, 4, 12, 28, 24, 928635)
        resolver_data = (tiled_jp2, 'jp2', lastmod)
        with patch.object(IIIFRequest, '_resolve_identifier', return_value=resolver_data):
            request1 = InfoRequest('fakeid')
            request2 = InfoRequest('fakeid')
            request1.etag == request2.etag
