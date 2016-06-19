
def st(it):
    # Make a sorted tuple. Sorting makes testing easier.
    return tuple(sorted(it))

class Compliance(object):
    # Loris will always be level 0, meaning that we don't worry about level 0
    # features here.
    REGION_LEVEL_1 = ('regionByPx',)
    REGION_LEVEL_2 = st(REGION_LEVEL_1 + ('regionByPct',))
    REGION_ALL = st(REGION_LEVEL_2 + ('regionSquare',))
    SIZE_LEVEL_1 = st(('sizeByW', 'sizeByH', 'sizeByPct'))
    SIZE_LEVEL_2 = st(
        SIZE_LEVEL_1 +
        ('sizeByConfinedWh', 'sizeByDistortedWh', 'sizeByWh')
    )
    SIZE_ALL = st(SIZE_LEVEL_2 + ('max','sizeAboveFull'))
    ROTATION_LEVEL_2 = ('rotationBy90s',)
    ROTATION_ALL = st(ROTATION_LEVEL_2 + ('rotationArbitrary', 'mirroring'))
    QUALITY_LEVEL_0 = ('default',)
    QUALITY_LEVEL_2 = st(('color', 'gray', 'bitonal'))
    QUALITY_ALL = QUALITY_LEVEL_2
    FORMAT_LEVEL_0 = ('jpg',)
    FORMAT_LEVEL_2 = ('png',)
    FORMAT_ALL = st(FORMAT_LEVEL_2 + ('webp',)) # this is specific to loris
    HTTP_LEVEL_1 = ('baseUriRedirect', 'cors', 'jsonldMediaType')
    HTTP_LEVEL_2 = HTTP_LEVEL_1
    HTTP_ALL = st(HTTP_LEVEL_2 + ('profileLinkHeader', 'canonicalLinkHeader'))
    ALL_LEVEL_1 = st(
        REGION_LEVEL_1 + SIZE_LEVEL_1 + HTTP_LEVEL_1
    )
    ALL_LEVEL_2 = st(
        REGION_LEVEL_2 + SIZE_LEVEL_2 + ROTATION_LEVEL_2 + QUALITY_LEVEL_2 +
        FORMAT_LEVEL_2 + HTTP_LEVEL_2
    )

    def __init__(self, config):
        self.config = config
        self._server_compliance = None
        self._additional_features = None
        self._region_features = None
        self._size_features = None
        self._rotation_features = None
        self._quality_features = None
        self._format_features = None
        self._http_features = None
        self._scale_factors_only = None
        self._scale_factors_only_width = None
        self._scale_factors_only_height = None
        self._compliance_uri = None

    @property
    def server_compliance(self):
        # Determine the copmliance level based on
        if self._server_compliance is None:
            self._server_compliance = min(
                self._region_level,
                self._size_level,
                self._rotation_level,
                self._quality_level,
                self._format_level,
                self._http_level
            )
        return self._server_compliance

    @property
    def compliance_uri(self):
        if self._compliance_uri is None:
            level = self.server_compliance
            uri = 'http://iiif.io/api/image/2/level{}.json'.format(level)
            self._compliance_uri = uri
        return self._compliance_uri

    @property
    def additional_features(self):
        # Features supported above the calculated compliance level, i.e. the
        # difference between all enabled features and the calculated compliance
        # level. For listing in profile[1]['supports'].
        if self._additional_features is None:
            level_features = set(()) # 0
            if self.server_compliance == 2:
                level_features = set(Compliance.ALL_LEVEL_2)
            elif self.server_compliance == 1:
                level_features = set(Compliance.ALL_LEVEL_1)
            self._additional_features = set(self.all_enabled_features) - level_features
        return st(self._additional_features)

    @property
    def all_enabled_features(self):
        return st(
            self.region_features +
            self.size_features +
            self.rotation_features +
            self.http_features
        )

    def to_profile(self, include_color=True):
        # A list suitable for placing in the "supports" key of info.json
        # Pass include_color=False if the source image is grayscale
        qualities = st(Compliance.QUALITY_LEVEL_0 + self.quality_features)
        if not include_color:
            qualities = st(q for q in qualities if q != 'color')
        d = {
            "supports" : self.additional_features,
            "qualities" : qualities,
            "formats" :  Compliance.FORMAT_LEVEL_0 + self.format_features
        }
        l = [ self.compliance_uri, d ]
        return l

    @property
    def region_features(self):
        # This is a list of features the config actually supports, regardless
        # of level. See http://iiif.io/api/image/2.1/compliance/#region
        # This should be passed to the RegionParameter constructor.
        if self._region_features is None:
            self._region_features = Compliance._filter_out_falses(self.config['region'])
        return self._region_features

    @property
    def _region_level(self):
        if self._region_is_2:
            return 2
        elif self._region_is_1:
            return 1
        else:
            return 0

    @property
    def _region_is_2(self):
        return all(r in self.region_features for r in Compliance.REGION_LEVEL_2)

    @property
    def _region_is_1(self):
        return all(r in self.region_features for r in Compliance.REGION_LEVEL_1)

    @property
    def size_features(self):
        if self._size_features is None:
            self._size_features = Compliance._filter_out_falses(self.config['size'])
        return self._size_features

    @property
    def _size_level(self):
        if self._size_is_2:
            return 2
        elif self._size_is_1:
            return 1
        else:
            return 0

    @property
    def _size_is_2(self):
        return all(r in self.size_features for r in Compliance.SIZE_LEVEL_2)

    @property
    def _size_is_1(self):
        return all(r in self.size_features for r in Compliance.SIZE_LEVEL_1)

    @property
    def rotation_features(self):
        if self._rotation_features is None:
            self._rotation_features = Compliance._filter_out_falses(self.config['rotation'])
        return self._rotation_features

    @property
    def _rotation_level(self):
        # rotation level 0 is the same as rotation level 1
        if self._rotation_is_2:
            return 2
        else:
            return 1

    @property
    def _rotation_is_2(self):
        return all(r in self.rotation_features for r in Compliance.ROTATION_LEVEL_2)

    @property
    def quality_features(self):
        if self._quality_features is None:
            self._quality_features = Compliance._filter_out_falses(self.config['quality'])
        return self._quality_features

    @property
    def _quality_level(self):
        # quality level 0 is the same as quality level 1
        if self._quality_is_2:
            return 2
        else:
            return 1

    @property
    def _quality_is_2(self):
        return all(r in self.quality_features for r in Compliance.QUALITY_LEVEL_2)

    @property
    def format_features(self):
        if self._format_features is None:
            self._format_features = Compliance._filter_out_falses(self.config['formats'])
        return self._format_features

    @property
    def _format_level(self):
        # format level 0 is the same as format level 1
        if self._format_is_2:
            return 2
        else:
            return 1

    @property
    def _format_is_2(self):
        return all(r in self.format_features for r in Compliance.FORMAT_LEVEL_2)

    @property
    def http_features(self):
        if self._http_features is None:
            self._http_features = Compliance._filter_out_falses(self.config['http'])
        return self._http_features

    @property
    def _http_level(self):
        # http level 1 is the same as level 2
        if self._http_is_2:
            return 2
        else:
            return 0

    @property
    def _http_is_2(self):
        return all(r in self.http_features for r in Compliance.HTTP_LEVEL_2)

    @property
    def scale_factors_only(self):
        # See http://iiif.io/api/image/2.1/compliance/#level-0-compliance
        # Only do the check if compliance is level 0, otherwise return False.
        level0 = self.server_compliance == 0
        if self._scale_factors_only is None and level0:
            enabled = self.config['size']['scaleFactors']['enabled']
            self._scale_factors_only = enabled
        else:
            self._scale_factors_only = False
        return self._scale_factors_only

    @property
    def scale_factors_only_width(self):
        # See http://iiif.io/api/image/2.1/compliance/#level-0-compliance
        # Only do the check if compliance is level 0, otherwise return None.
        level0 = self.server_compliance == 0
        if self._scale_factors_only_width is None and level0:
            w = self.config['size']['scaleFactors']['tileWidth']
            self._scale_factors_only_width = w
        return self._scale_factors_only_width

    @property
    def scale_factors_only_height(self):
        # See http://iiif.io/api/image/2.1/compliance/#level-0-compliance
        # Only do the check if compliance is level 0, otherwise return None.
        level0 = self.server_compliance == 0
        if self._scale_factors_only_height is None and level0:
            h = self.config['size']['scaleFactors']['tileHeight']
            self._scale_factors_only_height = h
        return self._scale_factors_only_height

    @staticmethod
    def _filter_out_falses(dict):
        # Takes e.g.:
        #   {
        #     'regionByPx': { 'enabled': True },
        #     'regionByPct': { 'enabled': True },
        #     'regionSquare': { 'enabled': True }
        #   }
        # and returns a tuple of the keys for which enabled is True.
        # (keys are sorted to make this method easier to test)
        keys = sorted(k for k,v in dict.items() if v['enabled'])
        try:
            keys.remove('scaleFactors') # this is a special case
        except ValueError:
            pass
        return tuple(keys)
