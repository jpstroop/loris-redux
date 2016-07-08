from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet

class HttpCompliance(AbstractFeatureSet):

    LEVEL_1 = ('baseUriRedirect', 'cors', 'jsonldMediaType')
    LEVEL_2 = LEVEL_1
    ALL = st(LEVEL_2 + ('profileLinkHeader', 'canonicalLinkHeader'))

    def __init__(self, config):
        super().__init__(config)
