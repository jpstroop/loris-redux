from abc import ABCMeta
from abc import abstractmethod


class AbstractParameter(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, uri_slice, enabled_features):
        self.uri_slice = uri_slice
        self.enabled_features = enabled_features
        self._canonical = None
        return

    @property
    @abstractmethod
    def canonical(self):  # pragma: no cover
        return

    def __str__(self):  # pragma: no cover
        return self.canonical
