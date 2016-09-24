#
# This helps us not have to pass so many things (caches, resolvers,
# transcoders...) around by letting us set class properties on the IIIFRequest
# at startup. Here's a basic example of how this pattern works:
#
# >>> class MyMeta(type): # Note we subclass type, not object
# ...     _something = None
# ...     def _get_something(self):
# ...         return self._something
# ...     def _set_something(self, value):
# ...         self._something = value
# ...     something = property(_get_something, _set_something)
# ...
# >>> class MyFoo(metaclass=MyMeta):
# ...     pass
# >>> print(MyFoo.something)
# None
# >>> MyFoo.something = 'bar'
# >>> MyFoo.something
# 'bar'
#

class MetaRequest(type):

    _compliance = None
    _info_cache = None
    _extractors = None
    _app_configs = None
    _transcoders = None
    _resolvers = None

    def _get_compliance(self):
        return self._compliance
    def _set_compliance(self, compliance):
        self._compliance = compliance
    compliance = property(_get_compliance, _set_compliance)

    def _get_info_cache(self):
        return self._info_cache
    def _set_info_cache(self, info_cache):
        self._info_cache = info_cache
    info_cache = property(_get_info_cache, _set_info_cache)

    def _get_extractors(self):
        return self._extractors
    def _set_extractors(self, extractors):
        self._extractors = extractors
    extractors = property(_get_extractors, _set_extractors)

    def _get_app_configs(self):
        return self._app_configs
    def _set_app_configs(self, app_configs):
        self._app_configs = app_configs
    app_configs = property(_get_app_configs, _set_app_configs)

    def _get_transcoders(self):
        return self._transcoders
    def _set_transcoders(self, transcoders):
        self._transcoders = transcoders
    transcoders = property(_get_transcoders, _set_transcoders)

    def _get_resolvers(self):
        return self._resolvers
    def _set_resolvers(self, resolvers):
        self._resolvers = resolvers
    resolvers = property(_get_resolvers, _set_resolvers)
