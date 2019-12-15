from loris.compliance.helpers import st
from loris.compliance.helpers import ComparableMixin

class AbstractFeatureSet(ComparableMixin):
    # Override these in implementations
    LEVEL_2 = ()
    LEVEL_1 = ()
    LEVEL_0 = () # Only necessary to overide if value are listed in the profile
    ALL = ()

    def __init__(self, config):
        self._config = config
        self._features = None

    @property
    def features(self):
        # This is a list of features the config actually supports, regardless
        # of level. See http://iiif.io/api/image/3.1/compliance/
        # This should be passed to the various Parameter constructors.
        if self._features is None:
            self._features = st(k for k,v in self._config.items() if v['enabled'])
        return self._features

    # This is here to that we can change features dynamically during tests. It
    # is not used in production
    @features.setter
    def features(self, features):
        self._features = features

    def __int__(self):
        if all(f in self.features for f in self.LEVEL_2):
            return 2
        elif all(f in self.features for f in self.LEVEL_1):
            return 1
        else:
            return 0
