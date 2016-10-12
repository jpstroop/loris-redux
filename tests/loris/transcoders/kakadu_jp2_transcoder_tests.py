from loris.transcoders.kakadu_jp2_transcoder import KakaduJp2Transcoder

from os.path import exists

class TestKakaduJp2Transcoder(object):

    def test_it_can_find_kakadu(self):
        lib, binary = KakaduJp2Transcoder._find_kakadu()
        assert exists(lib)
        assert lib.endswith('.so')
        assert exists(binary)
