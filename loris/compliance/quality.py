from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.constants import QUALITY_BITONAL
from loris.constants import QUALITY_COLOR
from loris.constants import QUALITY_GRAY

class QualityCompliance(AbstractFeatureSet):

    LEVEL_2 = st((QUALITY_COLOR, QUALITY_GRAY, QUALITY_BITONAL))
    ALL = LEVEL_2

    def __init__(self, config):
        super().__init__(config)
