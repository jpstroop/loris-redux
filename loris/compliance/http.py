from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.constants import BASE_URI_REDIRECT
from loris.constants import CORS
from loris.constants import JSONLD_MEDIA_TYPE
from loris.constants import PROFILE_LINK_HEADER
from loris.constants import CANONICAL_LINK_HEADER

class HttpCompliance(AbstractFeatureSet):

    LEVEL_1 = (BASE_URI_REDIRECT, CORS, JSONLD_MEDIA_TYPE)
    LEVEL_2 = LEVEL_1
    ALL = st(LEVEL_2 + (PROFILE_LINK_HEADER, CANONICAL_LINK_HEADER))

    def __init__(self, config):
        super().__init__(config)
