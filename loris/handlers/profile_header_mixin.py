from loris.constants import PROFILE_LINK_HEADER
from loris.requests.iiif_request import IIIFRequest

class ProfileHeaderMixin(object):

    @property
    def _profile_header_enabled(self):
        return PROFILE_LINK_HEADER in IIIFRequest.compliance.http.features

    @property
    def _profile_header(self):
        return f'<{IIIFRequest.compliance.uri}>;rel="profile"'
