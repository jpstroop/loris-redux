from loris.requests.meta_request import MetaRequest


class TestMetaRequest(object):

    def test_adds_compliance(self):
        class MyFoo(metaclass=MetaRequest):
            pass
        assert MyFoo.compliance is None
        MyFoo.compliance = 'whatever'
        assert MyFoo.compliance == 'whatever'

    def test_adds_info_cache(self):
        class MyFoo(metaclass=MetaRequest):
            pass
        assert MyFoo.info_cache is None
        MyFoo.info_cache = 'whatever'
        assert MyFoo.info_cache == 'whatever'

    def test_adds_extractors(self):
        class MyFoo(metaclass=MetaRequest):
            pass
        assert MyFoo.extractors is None
        MyFoo.extractors = 'whatever'
        assert MyFoo.extractors == 'whatever'

    def test_adds_app_configs(self):
        class MyFoo(metaclass=MetaRequest):
            pass
        assert MyFoo.app_configs is None
        MyFoo.app_configs = 'whatever'
        assert MyFoo.app_configs == 'whatever'

    def test_adds_transcoders(self):
        class MyFoo(metaclass=MetaRequest):
            pass
        assert MyFoo.transcoders is None
        MyFoo.transcoders = 'whatever'
        assert MyFoo.transcoders == 'whatever'
