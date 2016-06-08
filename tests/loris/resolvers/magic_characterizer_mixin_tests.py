import pytest
from loris.resolvers.magic_characterizer_mixin import MagicCharacterizerMixin
from loris.resolvers.api import AbstractResolver

class TestMagicCharacterizerMixin(object):

    # Fixtures (like tiled_jp2) are defined in ../conftest.py
    def test_works_with_jp2(self, tiled_jp2):
        assert MagicCharacterizerMixin.characterize(tiled_jp2) == 'jp2'

    def test_works_with_tiff(self, color_tif):
        assert MagicCharacterizerMixin.characterize(color_tif) == 'tif'

    def test_works_with_jpg(self, color_jpg):
        assert MagicCharacterizerMixin.characterize(color_jpg) == 'jpg'

    def test_works_with_png(self, color_png):
        assert MagicCharacterizerMixin.characterize(color_png) == 'png'

    def test_can_be_mixed_into_a_resolver(self, color_jpg):
        class MyResolver(AbstractResolver, MagicCharacterizerMixin):

            def is_resolvable(self, ident):
                return True
            def resolve(self, ident):
                fmt = MyResolver.characterize(color_jpg)
                return (color_jpg, fmt)

        resolver = MyResolver()
        assert resolver.resolve(color_jpg) == (color_jpg, 'jpg')
