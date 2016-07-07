import pytest
from loris.helpers.compliance import Compliance

class TestCompliance(object):

    def test__filter_out_falses(self):
        ex = {
            'regionByPx': { 'enabled': True },
            'regionByPct': { 'enabled': False },
            'regionSquare': { 'enabled': True }
        }
        true_keys = ('regionByPx', 'regionSquare')
        assert Compliance._filter_out_falses(ex) == true_keys

    def test__region_is_2(self):
        cfg = {
            'region' : {
                'regionByPx': { 'enabled': True },
                'regionByPct': { 'enabled': True },
                'regionSquare': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._region_is_2

    def test__region_is_2_false(self):
        cfg = {
            'region' : {
                'regionByPx': { 'enabled': True },
                'regionByPct': { 'enabled': False },
                'regionSquare': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._region_is_2 is False

    def test__region_is_1(self):
        cfg = {
            'region' : {
                'regionByPx': { 'enabled': True },
                'regionByPct': { 'enabled': False },
                'regionSquare': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._region_is_1

    def test__region_is_1_false(self):
        cfg = {
            'region' : {
                'regionByPx': { 'enabled': False },
                'regionByPct': { 'enabled': False },
                'regionSquare': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._region_is_1 is False

    def test_region__level_2(self):
        cfg = {
            'region' : {
                'regionByPx': { 'enabled': True },
                'regionByPct': { 'enabled': True },
                'regionSquare': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._region_level == 2

    def test_region__level_1(self):
        cfg = {
            'region' : {
                'regionByPx': { 'enabled': True },
                'regionByPct': { 'enabled': False },
                'regionSquare': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._region_level == 1

    def test_region__level_1(self):
        cfg = {
            'region' : {
                'regionByPx': { 'enabled': False },
                'regionByPct': { 'enabled': False },
                'regionSquare': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._region_level == 0

    def test__size_is_2(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': True },
                'sizeByDistortedWh': { 'enabled': True },
                'sizeByWh': { 'enabled': True },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_2

    def test__size_is_2_false_wo_sizeByWh(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': True },
                'sizeByDistortedWh': { 'enabled': True },
                'sizeByWh': { 'enabled': False },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_2 is False

    def test__size_is_2_false_wo_sizeByDistortedWh(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': True },
                'sizeByDistortedWh': { 'enabled': False },
                'sizeByWh': { 'enabled': True },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_2 is False

    def test__size_is_2_false_wo_sizeByConfinedWh(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': False },
                'sizeByDistortedWh': { 'enabled': True },
                'sizeByWh': { 'enabled': True },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_2 is False

    def test__size_is_1(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': False },
                'sizeByDistortedWh': { 'enabled': False },
                'sizeByWh': { 'enabled': False },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_1

    def test__size_is_1_with_a_single_level_2_feature(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': True },
                'sizeByDistortedWh': { 'enabled': False },
                'sizeByWh': { 'enabled': False },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_1

    def test__size_is_1_false_wo_sizeByPct(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': False },
                'sizeByConfinedWh': { 'enabled': False },
                'sizeByDistortedWh': { 'enabled': False },
                'sizeByWh': { 'enabled': False },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_1 is False

    def test__size_is_1_false_wo_sizeByH(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': False },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': False },
                'sizeByDistortedWh': { 'enabled': False },
                'sizeByWh': { 'enabled': False },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_1 is False

    def test__size_is_1_false_wo_sizeByW(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': False },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': False },
                'sizeByDistortedWh': { 'enabled': False },
                'sizeByWh': { 'enabled': False },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_is_1 is False

    def test_size__level_2(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': True },
                'sizeByDistortedWh': { 'enabled': True },
                'sizeByWh': { 'enabled': True },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_level == 2

    def test_size__level_1(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': True },
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': False },  # because this
                'sizeByDistortedWh': { 'enabled': True },
                'sizeByWh': { 'enabled': True },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_level == 1

    def test_size__level_0(self):
        cfg = {
            'size': {
                'sizeByW': { 'enabled': True },
                'sizeByH': { 'enabled': False }, # because this
                'sizeByPct': { 'enabled': True },
                'sizeByConfinedWh': { 'enabled': True },
                'sizeByDistortedWh': { 'enabled': True },
                'sizeByWh': { 'enabled': True },
                'sizeAboveFull': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._size_level == 0

    def test__rotation_is_2(self):
        cfg = {
            'rotation' : {
                'rotationBy90s': { 'enabled': True },
                'rotationArbitrary': { 'enabled': True },
                'mirroring': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._rotation_is_2

    def test__rotation_is_2_false(self):
        cfg = {
            'rotation' : {
                'rotationBy90s': { 'enabled': False },
                'rotationArbitrary': { 'enabled': True },
                'mirroring': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._rotation_is_2 is False

    def test__rotation_level_2(self):
        cfg = {
            'rotation' : {
                'rotationBy90s': { 'enabled': True },
                'rotationArbitrary': { 'enabled': True },
                'mirroring': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._rotation_level == 2

    def test__rotation_level_1(self):
        cfg = {
            'rotation' : {
                'rotationBy90s': { 'enabled': False },
                'rotationArbitrary': { 'enabled': True },
                'mirroring': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._rotation_level == 1

    def test__quality_is_2(self):
        cfg = {
            'quality' : {
                'color': { 'enabled': True },
                'gray': { 'enabled': True },
                'bitonal': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._quality_is_2

    def test__quality_is_2_false(self):
        cfg = {
            'quality' : {
                'color': { 'enabled': True },
                'gray': { 'enabled': False },
                'bitonal': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._quality_is_2 is False

    def test__quality_level_2(self):
        cfg = {
            'quality' : {
                'color': { 'enabled': True },
                'gray': { 'enabled': True },
                'bitonal': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._quality_level == 2

    def test__quality_level_1(self):
        cfg = {
            'quality' : {
                'color': { 'enabled': False },
                'gray': { 'enabled': False },
                'bitonal': { 'enabled': False }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._quality_level == 1

    def test__format_is_2(self):
        cfg = {
            'formats' : {
                'png': { 'enabled': True },
                'webp': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._format_is_2

    def test__format_is_2_false(self):
        cfg = {
            'formats' : {
                'png': { 'enabled': False },
                'webp': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._format_is_2 is False

    def test__format_level_2(self):
        cfg = {
            'formats' : {
                'png': { 'enabled': True },
                'webp': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._format_level == 2

    def test__format_level_1(self):
        cfg = {
            'formats' : {
                'png': { 'enabled': False },
                'webp': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._format_level == 1

    def test__http_is_2(self):
        cfg = {
            'http': {
                'baseUriRedirect': { 'enabled': True },
                'cors': { 'enabled': True },
                'jsonldMediaType': { 'enabled': True },
                'profileLinkHeader': { 'enabled': True },
                'canonicalLinkHeader': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._http_is_2

    def test__http_is_2_false_wo_baseUriRedirect(self):
        cfg = {
            'http': {
                'baseUriRedirect': { 'enabled': False },
                'cors': { 'enabled': True },
                'jsonldMediaType': { 'enabled': True },
                'profileLinkHeader': { 'enabled': True },
                'canonicalLinkHeader': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._http_is_2 is False

    def test__http_is_2_false_wo_cors(self):
        cfg = {
            'http': {
                'baseUriRedirect': { 'enabled': True },
                'cors': { 'enabled': False },
                'jsonldMediaType': { 'enabled': True },
                'profileLinkHeader': { 'enabled': True },
                'canonicalLinkHeader': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._http_is_2 is False

    def test__http_is_2_false_wo_cors(self):
        cfg = {
            'http': {
                'baseUriRedirect': { 'enabled': True },
                'cors': { 'enabled': True },
                'jsonldMediaType': { 'enabled': False },
                'profileLinkHeader': { 'enabled': True },
                'canonicalLinkHeader': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._http_is_2 is False

    def test__http_level_2(self):
        cfg = {
            'http': {
                'baseUriRedirect': { 'enabled': True },
                'cors': { 'enabled': True },
                'jsonldMediaType': { 'enabled': True },
                'profileLinkHeader': { 'enabled': True },
                'canonicalLinkHeader': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._http_level == 2

    def test__http_level_2(self):
        cfg = {
            'http': {
                'baseUriRedirect': { 'enabled': False },
                'cors': { 'enabled': True },
                'jsonldMediaType': { 'enabled': True },
                'profileLinkHeader': { 'enabled': True },
                'canonicalLinkHeader': { 'enabled': True }
            }
        }
        compliance = Compliance(cfg)
        assert compliance._http_level == 0

    def test_compliance_uri(self, everything_enabled_json):
        compliance = Compliance(everything_enabled_json)
        uri = 'http://iiif.io/api/image/2/level2.json'
        assert compliance.compliance_uri == uri

    def test_profile0_plus_sizeByW_json(self, level0_plus_sizeByW_json):
        compliance = Compliance(level0_plus_sizeByW_json)
        expected = [
            'http://iiif.io/api/image/2/level0.json',
            {
                'formats': ('jpg',),
                'qualities': ('default',),
                "supports" : ("sizeByW",)
            }
        ]
        assert compliance.to_profile() == expected

    def test_profile2_plus_everything_json(self, everything_enabled_json):
        compliance = Compliance(everything_enabled_json)
        expected = [
            'http://iiif.io/api/image/2/level2.json',
            {
                'formats': ('jpg', 'png', 'webp'),
                'qualities': ('bitonal', 'color', 'default', 'gray'),
                "supports" : (
                    'canonicalLinkHeader',
                    'max',
                    'mirroring',
                    'profileLinkHeader',
                    'regionSquare',
                    'rotationArbitrary',
                    'sizeAboveFull'
                )
            }
        ]
        assert compliance.to_profile() == expected

    def test_profile2_plus_everything_json_no_color(self, everything_enabled_json):
        compliance = Compliance(everything_enabled_json)
        expected = [
            'http://iiif.io/api/image/2/level2.json',
            {
                'formats': ('jpg', 'png', 'webp'),
                'qualities': ('bitonal', 'default', 'gray'),
                "supports" : (
                    'canonicalLinkHeader',
                    'max',
                    'mirroring',
                    'profileLinkHeader',
                    'regionSquare',
                    'rotationArbitrary',
                    'sizeAboveFull'
                )
            }
        ]
        assert compliance.to_profile(include_color=False) == expected


    # these tests use fixtures defined in tests/conftest.py
    def test_level_2_if_everything(self, everything_enabled_json):
        compliance = Compliance(everything_enabled_json)
        assert int(compliance) == 2

    def test_service_compliance_1(self, everything_but_sizeByConfinedWh_json):
        compliance = Compliance(everything_but_sizeByConfinedWh_json)
        assert int(compliance) == 1

    def test_service_compliance_0(self, everything_but_regionByPx_json):
        compliance = Compliance(everything_but_regionByPx_json)
        assert int(compliance) == 0

    def test_additional_features_two_plus(self, level2_plus_json):
        compliance = Compliance(level2_plus_json)
        extras = ('max', 'regionSquare')
        assert int(compliance) == 2
        assert compliance.additional_features == extras

    def test_additional_features_one_plus_sizeByConfinedWh(self, level1_plus_sizeByConfinedWh_json):
        extras = ('sizeByConfinedWh',)
        compliance = Compliance(level1_plus_sizeByConfinedWh_json)
        assert int(compliance) == 1
        assert compliance.additional_features == extras

    def test_additional_features_0_plus_sizeByW(self, level0_plus_sizeByW_json):
        extras = ('sizeByW',)
        compliance = Compliance(level0_plus_sizeByW_json)
        assert int(compliance) == 0
        assert compliance.additional_features == extras
