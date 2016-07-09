from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet

class RotationCompliance(AbstractFeatureSet):

    LEVEL_2 = ('rotationBy90s',)
    ALL = st(LEVEL_2 + ('rotationArbitrary', 'mirroring'))

    def __init__(self, config):
        super().__init__(config)
