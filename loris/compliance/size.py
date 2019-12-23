from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.compliance.helpers import st
from loris.constants import FEATURE_SIZE_BY_CONFINED_WH
from loris.constants import FEATURE_SIZE_BY_H
from loris.constants import FEATURE_SIZE_BY_PCT
from loris.constants import FEATURE_SIZE_BY_W
from loris.constants import FEATURE_SIZE_BY_WH
from loris.constants import FEATURE_SIZE_UPSCALING


class SizeCompliance(AbstractFeatureSet):

    LEVEL_1 = st((FEATURE_SIZE_BY_W, FEATURE_SIZE_BY_H))
    LEVEL_2 = st(LEVEL_1 + (FEATURE_SIZE_BY_CONFINED_WH, FEATURE_SIZE_BY_WH, FEATURE_SIZE_BY_PCT))
    ALL = st(LEVEL_2 + (FEATURE_SIZE_UPSCALING,))

    def __init__(self, config):
        super().__init__(config)
