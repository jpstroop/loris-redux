from loris.constants import ROTATION_ARBITRARY
from loris.constants import ROTATION_BY_90S
from loris.constants import ROTATION_MIRRORING
from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.compliance.helpers import st

class RotationCompliance(AbstractFeatureSet):

    LEVEL_2 = (ROTATION_BY_90S,)
    ALL = st(LEVEL_2 + (ROTATION_ARBITRARY, ROTATION_MIRRORING))

    def __init__(self, config):
        super().__init__(config)
