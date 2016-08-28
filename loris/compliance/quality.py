from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.constants import BITONAL
from loris.constants import COLOR
from loris.constants import GRAY

class QualityCompliance(AbstractFeatureSet):

    LEVEL_2 = st((COLOR, GRAY, BITONAL))
    ALL = LEVEL_2

    def __init__(self, config):
        super().__init__(config)
