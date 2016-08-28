from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.compliance.helpers import st
from loris.constants import REGION_BY_PCT
from loris.constants import REGION_BY_PIXEL
from loris.constants import REGION_SQUARE

class RegionCompliance(AbstractFeatureSet):

    LEVEL_1 = (REGION_BY_PIXEL,)
    LEVEL_2 = st(LEVEL_1 + (REGION_BY_PCT,))
    ALL = st(LEVEL_2 + (REGION_SQUARE,))

    def __init__(self, config):
        super().__init__(config)
