from collections import deque
from loris.info.abstract_extractor import AbstractExtractor
from loris.info.structs.size import Size
from loris.info.structs.tile import Tile
from math import ceil


class Jp2Extractor(AbstractExtractor):
    # Extracts JPEG 2000 specific info for an image
    def __init__(self, compliance, app_configs):
        super().__init__(compliance, app_configs)
        self._include_tiles_and_sizes = None

    def extract(self, path, http_identifier):
        metadata = Jp2Parser(path).metadata
        info = self.init_info(http_identifier)
        info.width = metadata["image_width"]
        info.height = metadata["image_height"]
        info.identifier = http_identifier
        max_size = self.max_size(info.width, info.height)
        info.sizes = [max_size]
        if self.include_tiles_and_sizes:
            info.tiles = Jp2Extractor._format_tiles(metadata)
            level_sizes = Jp2Extractor._levels_to_sizes(
                metadata["levels"], info.width, info.height, max_size.width, max_size.height
            )
            # Don't include the full w/h again:
            if max_size.width == info.width:
                info.sizes.extend(level_sizes[1:])
            else:
                info.sizes.extend(level_sizes)

        quals = self.compliance.extra_qualities(metadata["is_color"])
        info.extra_qualities = quals
        return info

    @property
    def include_tiles_and_sizes(self):
        if self._include_tiles_and_sizes is None:
            encoded_only = self.app_configs["sizes_and_tiles"]["jp2"]["encoded_only"]
            self._include_tiles_and_sizes = (self.compliance > 0) or encoded_only
        return self._include_tiles_and_sizes

    @staticmethod
    def _levels_to_sizes(levels, w, h, max_w, max_h):
        sizes = []
        for _ in range(0, levels):
            if w <= max_w and h <= max_h:
                sizes.append(Size(w, h))
            # Kakadu uses the ceiling when the number of levels to discard
            # is passed as -reduce, i.e. Given an image that is 7200 x 5906:
            # kdu_expand -i my_img.jp2 -o out.bmp -reduce 3
            # makes an image that is 900 x __739__, even though
            # (((5906 / 2) / 2) / 2) = 738 and
            # (((5906 / 2.0) / 2.0) / 2.0) = 738.25
            # This may be different in openjpeg and the rounding method will
            # need to be parameterized if so.
            w = ceil(w / 2.0)
            h = ceil(h / 2.0)
        return sizes

    @staticmethod
    def _format_tiles(metadata):
        tiles = None
        if "precincts" in metadata:
            tiles = Jp2Extractor._tiles_from_jp2_precincts(metadata["precincts"])
        elif "tile_width" in metadata:
            w = metadata["tile_width"]
            h = metadata["tile_height"]
            l = metadata["levels"]
            tiles = Jp2Extractor._tiles_from_jp2_tiles(w, h, l)
        return tiles

    @staticmethod
    def _tiles_from_jp2_precincts(precinct_list):
        # this is just...gross. Starts w/:
        # ( (w,h), (w,h), (w,h), (w,h), (w,h), (w,h) ) sorted by level 1-n
        groups = {}
        for scale, size in [(2 ** i, e) for i, e in enumerate(precinct_list)]:
            if size in groups:
                groups[size].append(scale)
            else:
                groups[size] = [scale]
        # Now we have, e.g.:
        # {(128, 128): [4, 8, 16, 32], (512, 512): [1], (256, 256): [2]}
        tiles = []
        for size in sorted(groups.keys(), reverse=True):
            tiles.append(Tile(size[0], groups[size], size[1]))
        return tiles

    @staticmethod
    def _tiles_from_jp2_tiles(width, height, levels):
        scale_factors = [2 ** l for l in range(0, levels)]
        return [Tile(width, scale_factors, height)]


class Jp2Parser(object):
    # Getting metadata out of a jp2 is complex enough, without having to deal
    # with the rest of the application. This makes jp2 info extraction easier to
    # test as well.
    # "Pg. N" annotations throughout refer to ISO/IEC 15444-1:2004 (E).
    # ISO/IEC 15444-2:2004 (Jp2 Extensions) is referenced once when dealing with
    # color profiles.

    SOC = b"\xff\x4f"  # SOC (start of codestream), pg. 19
    SIZ = b"\xff\x51"  # SIZ (image and tile siz), pg. 21
    COD = b"\xff\x52"  # COD (coding style default), pg. 22
    IHDR = b"\x69\x68\x64\x72"  # I.5.3.1 Image Header box, pg. 136
    COLR = b"\x63\x6F\x6C\x72"  # I.5.3.3 Color Specification Box, pg. 138

    def __init__(self, path):
        self.path = path

    @staticmethod
    def read_int(b_b_bytes):
        return int.from_bytes(b_b_bytes, byteorder="big", signed=False)

    @staticmethod
    def read_to_marker(jp2, marker):
        window_size = len(marker)
        window = deque([jp2.read(window_size)], window_size)
        while bytes(b"".join(window)) != marker:
            window.append(jp2.read(1))

    @staticmethod
    def read_precint_wh(jp2):
        # See table A.21 on pg. 26.
        b = Jp2Parser.read_int(jp2.read(1))
        w = 2 ** (b & 15)  # 4 LSBs are the precinct width exponent
        h = 2 ** (b >> 4)  # 4 MSBs are the precinct height exponent
        return (w, h)  # Easier to group later if this is hashable (dicts are not)

    @property
    def metadata(self):
        # This gets a little long, but breaking it up any more would probably
        # lead to more confusion.
        info = {}
        with open(self.path, "rb") as jp2:
            Jp2Parser.read_to_marker(jp2, Jp2Parser.IHDR)
            info["image_height"] = Jp2Parser.read_int(jp2.read(4))  # height (pg. 136)
            info["image_width"] = Jp2Parser.read_int(jp2.read(4))

            Jp2Parser.read_to_marker(jp2, Jp2Parser.COLR)
            colr_meth = Jp2Parser.read_int(jp2.read(1))  # METH (pg. 138)
            colr_prec = Jp2Parser.read_int(jp2.read(1))  # PREC (pg. 139)
            colr_approx = Jp2Parser.read_int(jp2.read(1))  # APPROX (pg. 139)
            if colr_meth == 1:
                enum_cs = Jp2Parser.read_int(jp2.read(4))
                if enum_cs == 16:  # sRGB
                    info["is_color"] = True
                elif enum_cs == 17:  # grayscale
                    info["is_color"] = False
                elif enum_cs == 18:  # sYCC pragma: no cover
                    msg = "Loris does not support sYCC colorspace"
                    raise Exception(msg)
                else:  # pragma: no cover
                    msg = 'Enumerated colorspace is neither "16", "17", or "18"'
                    raise Exception(msg)
            elif colr_meth == 2 or (
                colr_meth <= 4 and colr_prec <= 256 and 1 <= colr_approx <= 4
            ):  # pragma: no cover
                # This is an assumption, i.e. that if you have a color profile
                # embedded, you're probably working with color images.
                # UNTESTED
                info["is_color"] = True
                profile_size_bytes = jp2.read(4)
                profile_size = Jp2Parser.read_int(profile_size_bytes)
                bts = (profile_size_bytes, jp2.read(profile_size - 4))
                info["embedded_color_profile"] = b"".join(bts)
            else:  # sYCC
                raise Exception("Unable to determine color information")

            Jp2Parser.read_to_marker(jp2, Jp2Parser.SOC)
            Jp2Parser.read_to_marker(jp2, Jp2Parser.SIZ)
            jp2.read(20)  # Through Lsiz (16 bits), Rsiz (16), Xsiz (32),
            # Ysiz (32), XOsiz (32), and YOsiz (32)
            tw = Jp2Parser.read_int(jp2.read(4))
            th = Jp2Parser.read_int(jp2.read(4))
            if tw != info["image_width"] and th != info["image_height"]:
                info["tile_width"] = tw
                info["tile_height"] = th
            jp2.read(10)  # XTOsiz (32), YTOsiz (32), Csiz (16)

            Jp2Parser.read_to_marker(jp2, Jp2Parser.COD)
            jp2.read(7)  # through Lcod (16), Scod (8), SGcod (32)
            info["levels"] = Jp2Parser.read_int(jp2.read(1))
            jp2.read(4)  # through the rest of the SPcod; see Table A.15, pg. 24.

            # We may have precincts if Scod or Scoc = xxxx xxx0
            # But we don't need to examine as this is the last variable in the
            # COD segment. Instead check if the next byte == b'\xFF', which
            # would indicate that we've moved on to another section. If it is
            # not, or if the tile size was just the same as the image
            # dimensions then we probably have precincts.
            twth = ("tile_width", "tile_height")
            no_tiles = all([info.get(d) is None for d in twth])
            b = jp2.read(1)
            if b != b"\xFF" and no_tiles:
                # These come back in reverse order (smallest first) from what
                # you'd expect, which is confusing. Instead we reverse so that
                # the list 2**index is the scale factor
                info["precincts"] = []
                for _ in range(0, info["levels"]):
                    info["precincts"].append(Jp2Parser.read_precint_wh(jp2))
                info["precincts"].reverse()
        return info
