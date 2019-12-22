from loris.exceptions import ResolverException
from loris.resolvers.file_system_resolver import FileSystemResolver
from loris.resolvers.magic_characterizer_mixin import MagicCharacterizerMixin

from datetime import datetime
from unittest.mock import patch
from urllib.parse import quote_plus

import os
import pytest

TUES_DT = datetime(2016, 9, 6, 6, 5, 4).timestamp()
WED_DT = datetime(2016, 9, 7, 6, 5, 4).timestamp()
THURS_DT = datetime(2016, 9, 8, 6, 5, 4).timestamp()
FRI_DT = datetime(2016, 9, 10, 6, 5, 4).timestamp()
FAKE_FILESTORE = '/tmp/fake_filestore'

def touch(fname, time=None):
    # not a real equivalent to `touch`, but close enough
    flags = os.O_CREAT | os.O_APPEND
    time = datetime.now().timestamp() if time is None else time
    with os.fdopen(os.open(fname, flags=flags, mode=0o666)) as f:
        path = f.fileno() if os.utime in os.supports_fd else fname
        os.utime(path, times=(time, time))
        return fname

@pytest.fixture(scope='function')
def fake_file(request):
    if not os.path.isdir(FAKE_FILESTORE):
        os.mkdir(FAKE_FILESTORE)
    name = 'wed.jp2'
    path = os.path.join(FAKE_FILESTORE, name)
    yield touch(path, time=WED_DT)
    # this is the teardown code (removes the files):
    os.unlink(path)
    os.rmdir(FAKE_FILESTORE)

@pytest.fixture(scope='function')
def fake_files(request):
    # returns paths three files exactly a day apart, oldest first
    os.mkdir(FAKE_FILESTORE)
    names = ('tues.jp2', 'wed.jp2', 'thurs.jp2', 'fri.jp2')
    paths = [os.path.join(FAKE_FILESTORE, name) for name in names]
    paths_times = (
        (paths[0], TUES_DT),
        (paths[1], WED_DT),
        (paths[2], THURS_DT),
        (paths[3], FRI_DT)
    )
    yield [touch(path, time) for path, time in paths_times]
    # this is the teardown code (removes the files):
    list(map(os.unlink, paths))
    os.rmdir(FAKE_FILESTORE)

class TestFileSystemResolver(object):

    def test_resolve_minimum_config(self, region_test_jp2, fixtures_dir):
        resolver = FileSystemResolver({'root' : fixtures_dir})
        relative_path = region_test_jp2.replace(fixtures_dir, '')[1:] # rm leading /
        identifier = quote_plus(relative_path)
        info = resolver.resolve(identifier)
        assert info[0] == region_test_jp2
        assert info[1] == 'jp2'
        assert info[2] == datetime.fromtimestamp(os.stat(region_test_jp2).st_mtime)

    def test_resolve_will_raise(self):
        resolver = FileSystemResolver({'root' : '/tmp'})
        with pytest.raises(ResolverException) as re:
            resolver.resolve('abcxyz.jp2')
        assert 'Could not resolve identifier: abcxyz.jp2' == re.value.message

    def test_is_resolveable(self, region_test_jp2, fixtures_dir):
        config = {
            'root' : fixtures_dir,
            'format_suffix' : 'jp2'
        }
        resolver = FileSystemResolver(config)
        relative_path = region_test_jp2.replace(fixtures_dir, '')[1:] # rm leading /
        identifier = quote_plus(relative_path.split('.')[0]) # rm '.jp2' and encode
        assert resolver.is_resolvable(identifier)

    @patch.object(FileSystemResolver, 'characterize')
    def test__sync_to_cache(self, patched_characterize, fake_file):
        patched_characterize.return_value = 'jp2'
        try:
            config = {
                'root' : FAKE_FILESTORE,
                'format_suffix' : 'jp2',
                'cache' : True
            }
            resolver = FileSystemResolver(config)
            original_file = fake_file
            fake_id = 'myid'
            # add the file to the cache (makes a copy)
            cached_path = resolver._sync_to_cache(fake_id, original_file)
            # check that it's in the cache (on the fs AND can be retrived by id)
            assert os.path.exists(cached_path)
            assert fake_id in resolver._cache_map
            # now write something to the original_file, which updates its timestamp
            message = 'in a bottle'
            with open(original_file, 'w') as f:
                print(message, file=f)
            assert os.stat(original_file).st_mtime > os.stat(cached_path).st_mtime
            # now try to get from the cache again
            new_cached_path = resolver._sync_to_cache(fake_id, original_file)
            # check that we have a new path:
            assert new_cached_path != cached_path
            # check that the old file no longer exists:
            assert not os.path.exists(cached_path)
            # check that the new file is in the cache by reading the contents
            contents = ''
            with open(new_cached_path, 'r') as f:
                contents = f.read().replace('\n', '')
            assert contents == message
        finally:
            resolver.purge_cache() # clean up!

    @patch.object(FileSystemResolver, 'characterize')
    def test_cache_map_in_sync_with_files(self, patched_characterize, fake_files):
        patched_characterize.return_value = 'jp2'
        try:
            f0, f1, f2, f3 = fake_files
            config = {
                'root' : FAKE_FILESTORE,
                'format_suffix' : 'jp2',
                'cache' : True,
                'cache_size' : 3
            }
            resolver = FileSystemResolver(config)
            first_file_path = resolver._sync_to_cache('id0', f0)
            resolver._sync_to_cache('id1', f1)
            resolver._sync_to_cache('id2', f2)
            assert len(resolver._list_cached_files()) == 3
            assert len(resolver._cache_map) == 3
            resolver._sync_to_cache('id3', f3)
            assert len(resolver._list_cached_files()) == 3
            assert len(resolver._cache_map) == 3
            assert 'id0' not in resolver._cache_map
            assert not os.path.exists(first_file_path)
        finally:
            resolver.purge_cache()

    def test__we_don_not_require_format_suffix(self, tiled_jp2):
        try:
            config = {
                'root' : FAKE_FILESTORE,
                'cache' : True,
            }
            resolver = FileSystemResolver(config)
            cached_path = resolver._sync_to_cache('myId', tiled_jp2)
            assert cached_path[-4:] == '.jp2'
        finally:
            resolver.purge_cache()

    def test__get_file_path(self):
        config = {
            'root' : '/tmp',
            'format_suffix' : 'jp2'
        }
        resolver = FileSystemResolver(config)
        assert resolver._get_file_path('foo%2Fbar') == '/tmp/foo/bar.jp2'
