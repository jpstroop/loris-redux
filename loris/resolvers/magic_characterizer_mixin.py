from logging import getLogger
from loris.exceptions import UnsupportedFormat
from loris.helpers.classproperty import classproperty
from loris.helpers.safe_lru_dict import SafeLruDict
from magic import from_file

logger = getLogger('loris')

class MagicCharacterizerMixin(object):

    supported_formats = {
        'image/jpeg' : 'jpg',
        'image/png' : 'png',
        'image/tiff' : 'tif',
        'image/jp2' : 'jp2'
        # TODO: jpf?
    }

    @staticmethod
    def characterize(file_path, supported_formats=supported_formats):
        fmt = MagicCharacterizerMixin._cache.get(file_path)
        if fmt is not None:
            return fmt
        else:
            return MagicCharacterizerMixin._get_and_cache(file_path, supported_formats)

    @classproperty
    def _cache():
        try:
            return MagicCharacterizerMixin._format_cache
        except AttributeError:
            logger.debug('format cache initialized')
            MagicCharacterizerMixin._format_cache = SafeLruDict(200)
            return MagicCharacterizerMixin._format_cache

    @staticmethod
    def _get_and_cache(file_path, supported_formats):
        mime_type = from_file(file_path, mime=True)
        try:
            fmt = supported_formats[mime_type]
            MagicCharacterizerMixin._cache[file_path] = fmt
            return fmt
        except KeyError:
            message = '{0} characterized as {1} format, which is not supported'
            message = message.format(file_path, mime_type)
            raise UnsupportedFormat(message, http_status_code=500)
