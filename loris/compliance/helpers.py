def st(it):
    # Make a sorted tuple. Sorting makes testing easier.
    return tuple(sorted(it))

class ComparableMixin(object):
    # Make it possible to do comparisons with an int w/o casting. Classes must
    # implement __int__(self)
    def __lt__(self, an_int):
        return int(self) < an_int
    def __le__(self, an_int):
        return int(self) <= an_int
    def __eq__(self, an_int):
        return int(self) == an_int
    def __ne__(self, an_int):
        return int(self) != an_int
    def __gt__(self, an_int):
        return int(self) > an_int
    def __ge__(self, an_int):
        return int(self) >= an_int
