from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty

# See: https://docs.python.org/3.5/library/abc.html
# and: https://pymotw.com/2/abc/
#
# Parameters should subclass this, because they force all methods to be
# implemented, e.g.:
#
# >>> from loris.parameters.api import AbstractParameter
# >>> class FooParameter(AbstractParameter):
# ...     def __init__(self, uri_slice):
# ...         super(FooParameter, self).__init__(uri_slice)
# ...
# >>> foo_parameter = FooParameter('abc')
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: Can't instantiate abstract class FooParameter with abstract methods canonical
#
# But:
#
# >>> class FooParameter(AbstractParameter):
# ...     def __init__(self, uri_slice):
# ...         super(FooParameter, self).__init__(uri_slice)
# ...     @property
# ...     def canonical(self):
# ...         return self.original_request + '_canonical'
# ...
# >>> foo_parameter = FooParameter('abc')
# >>> foo_parameter.canonical
# 'abc_canonical'
# >>> str(foo_parameter)
# 'abc'

class AbstractParameter(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, uri_slice):
        self.original_request = uri_slice
        return

    @property
    @abstractmethod
    def canonical(self):
        return

    def __str__(self):
        return self.original_request
