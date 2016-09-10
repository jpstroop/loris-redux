from loris.requests.iiif_request import IIIFRequest

from unittest.mock import patch
import pytest

class TestIIIFRequest(object):

    # These are integration tests. If there are failures check th the imported
    # classes first.

    def test_etag_raises(self):
        resolver_data = (None, None, None)
        with patch.object(IIIFRequest, '_resolve_identifier', return_value=resolver_data):
            request = IIIFRequest('foo/bar')
            with pytest.raises(NotImplementedError) as nie:
                request.etag
            assert 'classes must implement #etag' in str(nie.value)

    def test_base_uri(self, app_configs):
        resolver_data = (None, None, None)
        with patch.object(IIIFRequest, '_resolve_identifier', return_value=resolver_data):
            request = IIIFRequest('foo/bar')
            assert request.base_uri == 'http://localhost/foo%2Fbar'

    def test_info(self, tiled_jp2, compliance_2, app_configs):
        resolver_data = (tiled_jp2, 'jp2', None)
        with patch.object(IIIFRequest, '_resolve_identifier', return_value=resolver_data):
            request = IIIFRequest('foo/bar')
            assert request.info.width == 5906
            assert 'foo%2Fbar' in IIIFRequest.info_cache
