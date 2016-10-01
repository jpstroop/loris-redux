from loris.helpers.import_class import import_class
from loris.resolvers.api import AbstractResolver

from inspect import getmro
from json import dumps
from logging import getLogger

logger = getLogger('loris')

class Resolvers(object):

    def __init__(self, resolver_list):
        # resolver_list is a list of dicts with the keys 'class', 'prefix', and
        # 'config'.
        self._resolvers = {}
        [ self.add_resolver(e['class'], e['prefix'], e['config'])
            for e in resolver_list ] # pylint:disable=expression-not-assigned

    def resolve(self, prefixed_identifier):
        parts = prefixed_identifier.split(':')
        prefix = parts[0]
        identifier = ':'.join(parts[1:])
        return self._resolvers[prefix].resolve[identifier]

    def add_resolver(self, class_name, prefix, config):
        ResolverClass = import_class(class_name)
        # TODO: should this exit if we get a type error?
        Resolvers._check_resolver_class(ResolverClass) # raises TypeError
        Resolvers._check_prefix_class(prefix) # raises TypeError
        instance = ResolverClass(config)
        self._resolvers[prefix] = instance
        logger.info('Added resolver %s with prefix "%s":', class_name, prefix)
        [ logger.debug('%s: %s', k,v) for k,v in config.items() ] # pylint:disable=expression-not-assigned

    @property
    def json(self):
        resolvers = []
        for prefix, resolver in self._resolvers.items():
            d = { }
            d['prefix'] = prefix
            d['description'] = resolver.description
            resolvers.append(d)
        return dumps(resolvers).encode('utf8')

    @staticmethod
    def _check_resolver_class(resolver_class):
        if AbstractResolver not in getmro(resolver_class):
            name = resolver_class.__name__
            msg = '{0} must subclass AbstractResolver'.format(name)
            raise TypeError(msg)

    @staticmethod
    def _check_prefix_class(key):
        kls = key.__class__
        if kls is not str:
            name = kls.__name__
            msg = 'Resolver prefixes must be strings, got {0}'.format(name)
            raise TypeError(msg)
