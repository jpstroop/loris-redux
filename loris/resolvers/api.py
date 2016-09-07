from abc import ABCMeta
from abc import abstractmethod
from logging import getLogger

# See an explanation about how these work in loris.parameters.api

logger = getLogger('loris')

class AbstractResolver(metaclass=ABCMeta):

    def __init__(self, config={}):
        self.__dict__ = { **self.__dict__, **config }
        logger.debug('Initialized %s.%s', __name__, self.__class__.__name__)

    @abstractmethod
    def is_resolvable(self, ident):  # pragma: no cover
        # The idea here is that in some scenarios it may be cheaper to check
        # that an id is resolvable than to actually resolve it. For example, in
        # an HTTP resolver, this could be a HEAD instead of a GET.
        # Return a boolean
        return

    @abstractmethod
    def resolve(self, ident):  # pragma: no cover
        # Return a path to a file that can be transformed/transcoded to fulfill
        # the request the format (str, str)
        #
        #  * The path to the file on the local system MUST be absolute.
        #  * Implemetations may want to mix in the MagicCharacterizerMixin to
        #    help acquire the format.
        #
        # __Note__: MUST raise an ResolverException if the file does not exist.
        # We can't enforce that here, so implementations should do so in their
        # tests.
        return
