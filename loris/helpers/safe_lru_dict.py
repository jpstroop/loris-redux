from collections import OrderedDict
from threading import Lock

class SafeLruDict(object):
    # Implements a thread-safe LRU cache in memory.
    #
    # For background, see:
    #  * http://bugs.python.org/issue11875#msg134089,
    #  * https://docs.python.org/3/reference/datamodel.html?emulating-container-types#emulating-container-types
    #  * https://docs.python.org/3/library/stdtypes.html#typesmapping
    #
    # We override these mutators to add a Lock():
    #
    #  * __init__ (we don't support any init args other than size)
    #  * get (because we move to front internally)
    #  * __getitem__ (to use our get() and raise a KeyError)
    #  * __setitem__ (to lock _and_ maintain the size)
    #  * __delitem__
    #  * clear
    #  * move_to_end
    #  * pop
    #  * popitem
    #  * setdefault
    #
    # and a couple of magic methods (__contains__, __len__, __str__, __repr__)
    # since getattr() doesn't seem to delgate them. The remaining methods are
    # delegated to the internal OrderedDict.

    def __init__(self, size=200):
        self._dict = OrderedDict()
        self._size = size
        self._lock = Lock()

    def __delitem__(self, key):
        with self._lock:
            del self._dict[key]

    def __getitem__(self, key):
        val = self.get(key) # takes care of the lock & move to front
        if val is None:
            raise KeyError
        return val

    def __setitem__(self, key, val):
        with self._lock:
            while len(self._dict) >= self._size:
                self._dict.popitem(last=False)
            self._dict[key] = val

    def clear(self):
        with self._lock:
            return self._dict.clear()

    def get(self, key, default=None):
        val = self._dict.get(key, default)
        if key in self._dict:
            with self._lock:
                self._dict.move_to_end(key, last=False)
        return val

    def move_to_end(self, key, last=True):
        with self._lock:
            return self._dict.move_to_end(key, last)

    def pop(self, key, default=None):
        with self._lock:
            if key in self._dict:
                return self._dict.pop(key)
            elif default is None:
                raise KeyError
            else:
                return default

    def popitem(self, last=True):
        with self._lock:
            return self._dict.popitem(last)

    def setdefault(self, key, default=None):
        with self._lock:
            return self._dict.setdefault(key, default)

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key):
        return key in self._dict

    def __str__(self):
        return str(self._dict)

    def __repr__(self):
        return repr(self._dict)

    # Delegate the methods we don't override or implement
    def __getattr__(self, attr):
        return getattr(self._dict, attr)
