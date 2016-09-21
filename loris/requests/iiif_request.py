from loris.requests.meta_request import MetaRequest

from logging import getLogger
from urllib.parse import quote_plus

logger = getLogger('loris')

class IIIFRequest(metaclass=MetaRequest):

    def __init__(self, identifier, iiif_params=None):
        self.identifier = quote_plus(identifier)
        self.iiif_params = iiif_params

        resolver_data = self._resolve_identifier(self.identifier)
        self.file_path = resolver_data[0]
        self.file_format = resolver_data[1]
        self.last_mod = resolver_data[2]

        self._info = None
        self._etag = None
        self._base_uri = None

    @property
    def info(self):
        if self._info is None: # We haven't memoized
            self._info = IIIFRequest.info_cache.get(self.identifier)
            if self._info is None: # Not in cache either
                extractor = IIIFRequest.extractors[self.file_format]
                self._info = extractor.extract(self.file_path, self.base_uri)
                IIIFRequest.info_cache[self.identifier] = self._info
                logger.info('Extracted info from %s', self.file_path)
        return self._info

    @property
    def etag(self):
        raise NotImplementedError('All Request classes must implement #etag')

    @property
    def base_uri(self):
        if self._base_uri is None:
            server_uri = IIIFRequest.app_configs['server_uri']
            self._base_uri = '/'.join((server_uri, self.identifier))
        return self._base_uri

    def _resolve_identifier(self):
        # TODO: work w/ resolvers.resolve, which should probably live in the
        # metaclass so that we can init at startup
        # should return (file_path str, file_format str, last_mod datetime)
        pass
