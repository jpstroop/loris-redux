from loris.resolvers import Resolvers
from loris.resolvers.file_system_resolver import FileSystemResolver
import pytest


class MyStupidResolver:
    def __init__(self):
        pass


class TestResolvers(object):
    def test_can_load_from_config(self):
        config = [
            {
                "class": "loris.resolvers.file_system_resolver.FileSystemResolver",
                "prefix": "a",
                "config": {
                    "root": "/fill/me/in",
                    "format_suffix": None,
                    "cache": False,
                    "cache_root": "/tmp",
                    "cache_size": 100,
                },
            }
        ]
        resolvers = Resolvers(config)
        assert "a" in resolvers._resolvers
        assert isinstance(resolvers._resolvers["a"], FileSystemResolver)
        assert resolvers._resolvers["a"].cache is False

    def test_add_resolver(self):
        resolvers = Resolvers([])
        klass = "loris.resolvers.file_system_resolver.FileSystemResolver"
        prefix = "a"
        config = {"root": "/fill/me/in"}
        resolvers.add_resolver(klass, prefix, config)
        assert "a" in resolvers._resolvers
        assert isinstance(resolvers._resolvers["a"], FileSystemResolver)

    def test_raises_if_not_an_abstract_resolver(self):
        resolvers = Resolvers([])
        with pytest.raises(TypeError) as te:
            klass = "tests.loris.resolvers.resolvers_tests.MyStupidResolver"
            resolvers.add_resolver(klass, "x", {})
        assert "MyStupidResolver must subclass AbstractResolver" == str(te.value)

    def test_raises_if_key_is_not_a_str(self):
        resolvers = Resolvers([])
        with pytest.raises(TypeError) as te:
            klass = "loris.resolvers.file_system_resolver.FileSystemResolver"
            resolvers.add_resolver(klass, 1, {})
        assert "Resolver prefixes must be strings, got int" == str(te.value)
