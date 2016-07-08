from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet

class RegionCompliance(AbstractFeatureSet):

    LEVEL_1 = ('regionByPx',)
    LEVEL_2 = st(LEVEL_1 + ('regionByPct',))
    ALL = st(LEVEL_2 + ('regionSquare',))

    def __init__(self, config):
        super().__init__(config)
