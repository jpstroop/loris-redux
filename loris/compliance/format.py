from loris.compliance.abstract_feature_set import AbstractFeatureSet
from loris.compliance.helpers import st
from loris.constants import EXTENSION_PNG
from loris.constants import EXTENSION_WEBP

class FormatCompliance(AbstractFeatureSet):

    LEVEL_2 = (EXTENSION_PNG,)
    ALL = st(LEVEL_2 + (EXTENSION_WEBP,)) # this is specific to loris, more could be added

    def __init__(self, config):
        super().__init__(config)
