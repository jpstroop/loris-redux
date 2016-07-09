from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet

class QualityCompliance(AbstractFeatureSet):

    LEVEL_2 = st(('color', 'gray', 'bitonal'))
    ALL = LEVEL_2

    def __init__(self, config):
        super().__init__(config)
