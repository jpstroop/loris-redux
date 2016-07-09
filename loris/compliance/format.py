from loris.compliance.helpers import st
from loris.compliance.abstract_feature_set import AbstractFeatureSet

class FormatCompliance(AbstractFeatureSet):

    LEVEL_2 = ('png',)
    ALL = st(LEVEL_2 + ('webp',)) # this is specific to loris, more could be added

    def __init__(self, config):
        super().__init__(config)
