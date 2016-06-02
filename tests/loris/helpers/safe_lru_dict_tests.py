from loris.helpers.safe_lru_dict import SafeLruDict
from collections import OrderedDict
import pytest

class TestSafeLruDict(object):

    # Note that most of these tests work with the internal _dict that the
    # class is wrapped around so that we're truly only testing one impl.
    # method at a time.

    def test_init_sets_size(self):
        d = SafeLruDict(10)
        assert d._size == 10

    def test_init_sets_default_size(self):
        d = SafeLruDict()
        assert d._size == 200

    def test_del(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        del d['a']
        assert 'a' not in d._dict

    def test__getitem__(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        assert d['a'] == 'b'

    def test__setitem__(self):
        d = SafeLruDict()
        d['a'] = 'b'
        assert 'a' in d._dict

    def test__setitem__maintains_size(self):
        size = 3
        d = SafeLruDict(size)
        d['a'] = 'b'
        d['c'] = 'd'
        d['e'] = 'f'
        d['g'] = 'h'
        assert len(d._dict) == size

    def test_clear(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d.clear()
        assert len(d._dict) == 0

    def test_get(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        assert d.get('c') == 'd'

    def test_get_accepts_default(self):
        d = SafeLruDict()
        assert d.get('a', 'b') == 'b'

    def test_get_returns_none_if_no_default(self):
        d = SafeLruDict()
        assert d.get('a') is None

    def test_get_moves_to_front(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        _ = d['c']
        assert d.popitem(last=False) == ('c', 'd')

    def test_move_to_end_defaults_to_last(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        d.move_to_end('a')
        assert d._dict.popitem(last=True) == ('a', 'b')

    def test_move_to_end_can_move_to_front(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        d.move_to_end('c', last=False)
        assert d._dict.popitem(last=False) == ('c', 'd')

    def test_pop(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        assert d.pop('c') == 'd'
        assert 'c' not in d._dict

    def test_pop_will_raise_keyerror(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        with pytest.raises(KeyError):
            _ = d.pop('e')

    def test_pop_with_default(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        assert d.pop('g', 'h') == 'h'

    def test_popitem_returns_someting(self):
        pairs = (('a','b'),('c','d'),('e','f'))
        d = SafeLruDict()
        d._dict = OrderedDict(pairs)
        pair = d.popitem()
        assert pair in pairs
        assert pair[0] not in d._dict

    def test_popitem_raises_key_error(self):
        d = SafeLruDict()
        with pytest.raises(KeyError):
            _ = d.popitem()

    def test_popitem_defaults_to_last(self):
        pairs = (('a','b'),('c','d'),('e','f'))
        d = SafeLruDict()
        d._dict = OrderedDict(pairs)
        pair = d.popitem()
        assert pair == pairs[-1]

    def test_popitem_can_do_first_last(self):
        pairs = (('a','b'),('c','d'),('e','f'))
        d = SafeLruDict()
        d._dict = OrderedDict(pairs)
        pair = d.popitem(last=False)
        assert pair == pairs[0]

    def test_setdefault_sets(self):
        # If key is in the dictionary, return its value. If not, insert key
        # with a value of default and return default. default defaults to None.
        d = SafeLruDict()
        d.setdefault('a','b')
        assert d._dict['a'] == 'b'

    def test_setdefault_gets(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        assert d.setdefault('a') == 'b'

    def test_setdefault_defaults_to_none(self):
        d = SafeLruDict()
        assert d.setdefault('a') is None

    def test__len__(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        assert len(d) == 3

    def test__contains__(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        assert 'c' in d

    def test__not_contains__(self):
        d = SafeLruDict()
        d._dict['a'] = 'b'
        d._dict['c'] = 'd'
        d._dict['e'] = 'f'
        assert 'h' not in d
