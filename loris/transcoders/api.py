from abc import ABCMeta
from abc import abstractmethod
from logging import getLogger

# See an explanation about how these work in loris.parameters.api (the pattern
# of having one instance per application is the same)

logger = getLogger("loris")


class AbstractTranscoder(metaclass=ABCMeta):
    def __init__(self, config={}):  # pylint:disable=dangerous-default-value
        self.__dict__ = {**self.__dict__, **config}
        # see https://docs.python.org/dev/whatsnew/3.5.html#pep-448-additional-unpacking-generalizations
        logger.debug("Initialized %s.%s", __name__, self.__class__.__name__)

    @abstractmethod
    def execute(self, image_request):  # pragma: no cover
        return
