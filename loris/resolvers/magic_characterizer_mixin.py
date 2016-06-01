from magic import from_file
from loris.exceptions.unsupported_format import UnsupportedFormat

class MagicCharacterizerMixin(object):

    supported_formats = {
        b'image/jpeg' : 'jpg',
        b'image/png' : 'png',
        b'image/tiff' : 'tif',
        b'image/jp2' : 'jp2'
        # TODO: jpf?
    }

    # TODO: add a dict for caching: { path : format }

    @staticmethod
    def characterize(file_path, supported_formats=supported_formats):
        mime_type = from_file(file_path, mime=True)
        try:
            return supported_formats[mime_type]
        except KeyError:
            message = '{0} characterized as {1} format, which is not supported'
            message = message.format(file_path, mime_type)
            raise UnsupportedFormat(message, http_status_code=500)
