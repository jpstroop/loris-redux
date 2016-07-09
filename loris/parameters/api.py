from abc import ABCMeta
from abc import abstractmethod

#
# See: https://docs.python.org/3.5/library/abc.html
# and: https://pymotw.com/2/abc/
#

class AbstractParameter(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, uri_slice, enabled_features, info_data):
        self.uri_slice = uri_slice
        self.enabled_features = enabled_features
        self.info_data = info_data
        self._canonical = None
        return

    @property
    @abstractmethod
    def canonical(self): # pragma: no cover
        return

    def __str__(self): # pragma: no cover
        return self._canonical
