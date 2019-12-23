from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.compliance.helpers import st
from loris.constants import FEATURE_BASE_URI_REDIRECT
from loris.constants import FEATURE_CANONICAL_LINK_HEADER
from loris.constants import FEATURE_CORS
from loris.constants import FEATURE_JSONLD_MEDIA_TYPE
from loris.constants import FEATURE_PROFILE_LINK_HEADER


class HttpCompliance(AbstractFeatureSet):

    LEVEL_1 = st((FEATURE_BASE_URI_REDIRECT, FEATURE_CORS, FEATURE_JSONLD_MEDIA_TYPE))
    LEVEL_2 = LEVEL_1
    ALL = st(LEVEL_2 + (FEATURE_PROFILE_LINK_HEADER, FEATURE_CANONICAL_LINK_HEADER))

    def __init__(self, config):
        super().__init__(config)
