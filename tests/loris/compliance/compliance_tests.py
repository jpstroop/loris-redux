import pytest
from loris.compliance import Compliance

class TestCompliance(object):

    def test_int_and_comparisons(self, everything_enabled_yaml):
        compliance = Compliance(everything_enabled_yaml)
        assert int(compliance) == 2
        assert compliance > 1
        assert compliance >= 2
        assert compliance < 3
        assert compliance <= 2
        assert compliance != 0
        assert compliance == 2

    def test_uri(self, everything_enabled_yaml):
        compliance = Compliance(everything_enabled_yaml)
        assert compliance.uri == 'http://iiif.io/api/image/2/level2.json'

    def test_profile0_plus_sizeByW_yaml(self, level0_plus_sizeByW_yaml):
        compliance = Compliance(level0_plus_sizeByW_yaml)
        expected = (
            'http://iiif.io/api/image/2/level0.json',
            {
                "supports" : ("sizeByW",)
            }
        )
        assert compliance.to_profile() == expected

    def test_profile2_plus_everything_yaml(self, everything_enabled_yaml):
        compliance = Compliance(everything_enabled_yaml)
        expected = (
            'http://iiif.io/api/image/2/level2.json',
            {
                'qualities': ('bitonal', 'color', 'gray'),
                'formats': ('png', 'webp'),
                "supports" : (
                    'canonicalLinkHeader',
                    'mirroring',
                    'profileLinkHeader',
                    'regionSquare',
                    'rotationArbitrary',
                    'sizeAboveFull'
                )
            }
        )
        assert compliance.to_profile() == expected

    def test_profile2_plus_everything_yaml_no_color(self, everything_enabled_yaml):
        compliance = Compliance(everything_enabled_yaml)
        expected = (
            'http://iiif.io/api/image/2/level2.json',
            {
                'formats': ('png', 'webp'),
                'qualities': ('bitonal', 'gray'),
                "supports" : (
                    'canonicalLinkHeader',
                    'mirroring',
                    'profileLinkHeader',
                    'regionSquare',
                    'rotationArbitrary',
                    'sizeAboveFull'
                )
            }
        )
        assert compliance.to_profile(include_color=False) == expected

    # these tests use fixtures defined in tests/conftest.py
    def test_level_2_if_everything(self, everything_enabled_yaml):
        compliance = Compliance(everything_enabled_yaml)
        assert compliance == 2

    def test_service_compliance_1(self, everything_but_sizeByConfinedWh_yaml):
        assert Compliance(everything_but_sizeByConfinedWh_yaml) == 1

    def test_service_compliance_0(self, everything_but_regionByPx_yaml):
        assert Compliance(everything_but_regionByPx_yaml) == 0

    def test_additional_features_two_plus(self, level2_plus_yaml):
        compliance = Compliance(level2_plus_yaml)
        extras = ('regionSquare',)
        assert compliance == 2
        assert compliance.additional_features == extras

    def test_additional_features_one_plus_sizeByConfinedWh(self, level1_plus_sizeByConfinedWh_yaml):
        extras = ('sizeByConfinedWh',)
        compliance = Compliance(level1_plus_sizeByConfinedWh_yaml)
        assert compliance == 1
        assert compliance.additional_features == extras

    def test_additional_features_0_plus_sizeByW(self, level0_plus_sizeByW_yaml):
        extras = ('sizeByW',)
        compliance = Compliance(level0_plus_sizeByW_yaml)
        assert compliance == 0
        assert compliance.additional_features == extras
