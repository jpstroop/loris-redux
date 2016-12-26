from loris.exceptions import ResolverException
from loris.helpers.safe_lru_dict import SafeLruDict
from loris.resolvers.api import AbstractResolver
from loris.resolvers.magic_characterizer_mixin import MagicCharacterizerMixin

from datetime import datetime
from logging import getLogger
from os import listdir
from os import makedirs
from os import remove
from os import stat
from os.path import exists
from os.path import join
from shutil import copy2
from urllib.parse import unquote
from uuid import uuid4

logger = getLogger('loris')

class FileSystemResolver(AbstractResolver, MagicCharacterizerMixin):

    def __init__(self, config):
        super().__init__(config)
        self.root = config['root']
        self.format_suffix = config.get('format_suffix')
        self.cache = config.get('cache', False)
        if self.cache:
            self.cache_root = config.get('cache_root', '/tmp/loris_tmp')
            self._cache_size = config.get('cache_size', 100)
            self._cache_map = SafeLruDict(self._cache_size)
            makedirs(self.cache_root, exist_ok=True)

    def is_resolvable(self, identifier):
        return exists(self._get_file_path(identifier))

    def resolve(self, identifier):
        # TODO: Note that the indentifier here lacks the prefix. Maybe it
        # should be passed in so that we can include it in exception messages?
        # Changes the whole API.
        file_path = self._get_file_path(identifier)
        if self.cache:
            file_path = self._sync_to_cache(identifier, file_path)
        try:
            last_mod = self._get_lastmod_datetime(file_path)
            fmt = FileSystemResolver.characterize(file_path)
        except FileNotFoundError:
            raise ResolverException(identifier)
        return (file_path, fmt, last_mod)

    def purge_cache(self):
        if self.cache:
            self._cache_map.clear()
            list(map(remove, self._list_cached_files()))

    # TODO: There's a ResolvedFile class that could be extracted here:
    # * src_path
    # * @property format
    # * @property last_mod (mtime) (always from the src)
    # * @property _src_last_mod (not memoized, checks every time referenced, for comparison)
    # * @property / setter cache_path
    # * @property _cached_last_mod
    # * cached_is_stale (_src_last_mod > _cached_last_mod)
    #
    # The cache could probably be extracted as well; only does basic CRUD and
    # could impl __get__, __set__, etc. It would be nice to hide the removal of
    # files a bit better.

    def _get_file_path(self, identifier):
        path = join(self.root, unquote(identifier))
        if self.format_suffix:
            path = '.'.join((path, self.format_suffix))
        return path

    def _sync_to_cache(self, identifier, file_path):
        cached_path = self._cache_map.get(identifier)
        if cached_path is None:
            return self._add_file_to_cache(identifier, file_path)
        elif self._cached_file_is_not_stale(file_path, cached_path):
            return cached_path
        else:
            del self._cache_map[identifier]
            remove(cached_path)
            return self._add_file_to_cache(identifier, file_path)

    def _add_file_to_cache(self, identifier, src_file_path):
        fmt = FileSystemResolver.characterize(src_file_path)
        cache_path = self._new_cache_file_path(fmt)
        if len(self._cache_map) >= self._cache_size:
            # the dict would remove the key anyway, but we need the path
            last_id, path = self._cache_map.popitem(last=True)  # pylint:disable=unused-variable
            remove(path)
        copy2(src_file_path, cache_path)
        self._cache_map[identifier] = cache_path
        return cache_path

    def _get_lastmod_datetime(self, file_path):
        return datetime.fromtimestamp(self._get_mtime(file_path))

    def _get_mtime(self, file_path):  # pragma: no cover
        return stat(file_path).st_mtime

    def _list_cached_files(self): # newest first
        if self.cache:
            paths = [join(self.cache_root, n) for n in listdir(self.cache_root)]
            sorted_paths = sorted(paths, key=self._get_mtime)
            return sorted_paths

    def _cached_file_is_not_stale(self, src_path, cached_path):
        return self._get_mtime(src_path) <= self._get_mtime(cached_path)

    def _new_cache_file_path(self, fmt):
        name = '.'.join((str(uuid4().hex), fmt))
        return join(self.cache_root, name)
