from loris.transcoders.openjpeg_jp2_transcoder import OpenJpegJp2Transcoder

from os.path import exists

class TestOpenJpegJp2Transcoder(object):

    def test_it_can_find_openjpeg(self):
        lib, binary = OpenJpegJp2Transcoder._find_openjpeg()
        assert exists(lib)
        assert lib.endswith('.so.2.1.2')
        assert exists(binary)
