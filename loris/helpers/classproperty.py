# use this as a decorator
# class classproperty(object):
    # def __init__(self, getter):
    #     self.getter = getter
    # def __get__(self, instance, owner):
    #     return self.getter(owner)
class classproperty(dict):
    def __init__(self, func):
        print("*"*80)
        print("Initialized " + str(func))
        print("*"*80)
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result
