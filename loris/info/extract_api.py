from abc import ABCMeta
from abc import abstractmethod

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
    # http_identifier = base_uri + urllib.quote_plus(identifier # accounting for trailing /
    # info = extractors[format].extract(path, http_identifier)
    #
    def __init__(self, compliance, base_uri):
        # The base URI is the URI that will be prepended to the identifier to
        # create the @id in the info.json. This way the server can sit behind
        # a cache or load balancer and the @id can resolve to that, rather than
        # the URL of the server running a particular application instance.
        self.compliance = compliance
        self.base_uri = base_uri

    @abstractmethod
    def extract(self, path, http_identifier):  # pragma: no cover
        # Must return a loris.info.data.InfoData object.
        return
