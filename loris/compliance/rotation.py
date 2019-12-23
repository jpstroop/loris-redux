from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.compliance.helpers import st
from loris.constants import FEATURE_ROTATION_ARBITRARY
from loris.constants import FEATURE_ROTATION_BY_90S
from loris.constants import FEATURE_ROTATION_MIRRORING


class RotationCompliance(AbstractFeatureSet):

    LEVEL_2 = (FEATURE_ROTATION_BY_90S,)
    ALL = st(LEVEL_2 + (FEATURE_ROTATION_ARBITRARY, FEATURE_ROTATION_MIRRORING))

    def __init__(self, config):
        super().__init__(config)
