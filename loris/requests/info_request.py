from hashlib import sha1
from loris.requests.iiif_request import IIIFRequest


class InfoRequest(IIIFRequest):
    def __init__(self, identifier):
        super().__init__(identifier, "info.json")

    def __str__(self):
        return str(self.info)

    @property
    def etag(self):
        if self._etag is None:
            last_mod = str(self.last_mod)
            b = bytes(last_mod + self.file_path, "utf-8")
            self._etag = sha1(b).hexdigest()
        return self._etag
