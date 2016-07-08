from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet

class SizeCompliance(AbstractFeatureSet):

    LEVEL_1 = st(('sizeByW', 'sizeByH', 'sizeByPct'))
    LEVEL_2 = st(LEVEL_1 + ('sizeByConfinedWh', 'sizeByDistortedWh', 'sizeByWh'))
    ALL = st(LEVEL_2 + ('max', 'sizeAboveFull'))

    def __init__(self, config):
        super().__init__(config)
