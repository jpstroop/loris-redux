from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.compliance.helpers import st
from loris.constants import MAX
from loris.constants import SIZE_ABOVE_FULL
from loris.constants import SIZE_BY_CONFINED_WH
from loris.constants import SIZE_BY_H
from loris.constants import SIZE_BY_PCT
from loris.constants import SIZE_BY_W
from loris.constants import SIZE_BY_WH

class SizeCompliance(AbstractFeatureSet):

    LEVEL_1 = st((SIZE_BY_W, SIZE_BY_H))
    LEVEL_2 = st(LEVEL_1 + (SIZE_BY_CONFINED_WH, SIZE_BY_WH, SIZE_BY_PCT))
    ALL = st(LEVEL_2 + (SIZE_ABOVE_FULL,))

    def __init__(self, config):
        super().__init__(config)
