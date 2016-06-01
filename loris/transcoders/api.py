from abc import ABCMeta
from abc import abstractmethod
from logging import getLogger

# See an explanation about how these work in loris.parameters.api

logger = getLogger('loris')

class AbstractTranscoder(metaclass=ABCMeta):

    # TODO: consider adding two static properties: input='fmt' and
    # outputs=('fmt', 'fmt')
    # The application could then have a transcoder registry that finds
    # transcoders dynamically based on the input. Maybe outputs isn't necessary? 

    def __init__(self, config={}):
        self.__dict__ = { **self.__dict__, **config }
        # see https://docs.python.org/dev/whatsnew/3.5.html#pep-448-additional-unpacking-generalizations
        logger.debug('Initialized %s.%s' % (__name__, self.__class__.__name__))

    @abstractmethod
    def transcode(self, src_file_path, target_file_path, image_request):
        # TODO: target_file_path could change or go away since we're not caching
        return
