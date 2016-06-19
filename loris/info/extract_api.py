from abc import ABCMeta
from abc import abstractmethod

BITONAL_QUALITIES = ('bitonal', 'default')
COLOR_QUALITIES = ('bitonal', 'color', 'default', 'gray')
GRAY_QUALITIES = ('bitonal', 'default', 'gray')

class AbstractExtractor(metaclass=ABCMeta):
    #
    # The InfoHandler has a static dict of these, one for each format we
    # support, e.g., at init:
    #
    # extractors = { 'jp2' : jp2extractor_instance, 'jpg' : ... }
    #
    # and then, for each request, the InfoHandler instance does something like:
    #
    # path, format = resolver.resvolve(identifier)
    # http_identifier = server_uri + urllib.quote_plus(identifier # accounting for trailing /
    # info = extractors[format].extract(path, http_identifier)
    #
    def __init__(self, compliance):
        self.compliance = compliance

    @abstractmethod
    def extract(self, path, http_identifier):  # pragma: no cover
        # Must return a loris.info.data.InfoData object.
        return
