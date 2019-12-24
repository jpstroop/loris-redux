from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.compliance.helpers import st
from loris.constants import FEATURE_REGION_BY_PCT
from loris.constants import FEATURE_REGION_BY_PIXEL
from loris.constants import FEATURE_REGION_SQUARE


class RegionCompliance(AbstractFeatureSet):

    LEVEL_1 = st((FEATURE_REGION_BY_PIXEL, FEATURE_REGION_SQUARE))
    LEVEL_2 = st(LEVEL_1 + (FEATURE_REGION_BY_PCT,))
    ALL = LEVEL_2

    def __init__(self, config):
        super().__init__(config)
