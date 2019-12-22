from decimal import Decimal

# strings
EXTENSION_JPG = 'jpg'
EXTENSION_PNG = 'png'
EXTENSION_WEBP = 'webp'
FEATURE_BASE_URI_REDIRECT = 'baseUriRedirect'
FEATURE_CANONICAL_LINK_HEADER = 'canonicalLinkHeader'
FEATURE_CORS = 'cors'
FEATURE_JSONLD_MEDIA_TYPE = 'jsonldMediaType'
FEATURE_PROFILE_LINK_HEADER = 'profileLinkHeader'
FEATURE_REGION_BY_PCT = 'regionByPct'
FEATURE_REGION_BY_PIXEL = 'regionByPx'
FEATURE_REGION_SQUARE = 'regionSquare'
FEATURE_ROTATION_ARBITRARY = 'rotationArbitrary'
FEATURE_ROTATION_BY_90S = 'rotationBy90s'
FEATURE_ROTATION_MIRRORING = 'mirroring'
FEATURE_SIZE_BY_CONFINED_WH = 'sizeByConfinedWh'
FEATURE_SIZE_BY_H = 'sizeByH'
FEATURE_SIZE_BY_PCT = 'sizeByPct'
FEATURE_SIZE_BY_W = 'sizeByW'
FEATURE_SIZE_BY_WH = 'sizeByWh'
FEATURE_SIZE_UPSCALING = 'sizeUpscaling'
HEADER_ACCEPT = 'accept'
HEADER_ACCESS_CONTROL_ALLOW_METHODS = 'access-control-allow-method'
HEADER_ACCESS_CONTROL_ALLOW_ORIGIN = 'access-control-allow-origin'
HEADER_ACCESS_CONTROL_HEADER_ALLOWS = 'access-control-allow-headers'
HEADER_ACCESS_CONTROL_MAX_AGE = 'access-control-max-age'
HEADER_ALLOW = 'allow'
HEADER_CONNECTION = "connection"
HEADER_CONTENT_TYPE = 'content-type'
HEADER_KEEP_ALIVE = 'keep-alive'
HEADER_VARY = 'vary'
KEYWORD_CONTEXT = '@context'
KEYWORD_DEFAULT = 'default'
KEYWORD_EXTRA_FEATURES = 'extraFeatures'
KEYWORD_EXTRA_FORMATS = 'extraFormats'
KEYWORD_EXTRA_QUALITIES = 'extraQualities'
KEYWORD_FULL = 'full'
KEYWORD_HEIGHT = 'height'
KEYWORD_ID = 'id'
KEYWORD_IMAGE_SERVICE_3 = 'ImageService3'
KEYWORD_MAX = 'max'
KEYWORD_MAX_AREA = 'maxArea'
KEYWORD_MAX_HEIGHT = 'maxHeight'
KEYWORD_MAX_WIDTH = 'maxWidth'
KEYWORD_PREFERRED_FORMATS = 'preferredFormats'
KEYWORD_PROFILE = 'profile'
KEYWORD_PROTOCOL = 'protocol'
KEYWORD_SCALE_FACTORS = 'scaleFactors'
KEYWORD_SIZES = 'sizes'
KEYWORD_SQUARE = 'square'
KEYWORD_TILES = 'tiles'
KEYWORD_TYPE = 'type'
KEYWORD_WIDTH = 'width'
MEDIA_TYPE_JPG = 'image/jpeg'
MEDIA_TYPE_JSON = 'application/json'
MEDIA_TYPE_JSONLD = 'application/ld+json;profile="http://iiif.io/api/image/3/context.json"'
MEDIA_TYPE_PNG = 'image/png'
MEDIA_TYPE_WEBP = 'image/webp'
QUALITY_BITONAL = 'bitonal'
QUALITY_COLOR = 'color'
QUALITY_GRAY = 'gray'
URI_COMPLIANCE_PAGE = 'http://iiif.io/api/image/3.1/compliance/#compliance'
URI_CONTEXT = 'http://iiif.io/api/image/3/context.json'
URI_PROTOCOL = 'http://iiif.io/api/image'

# numbers and objects
DECIMAL_ONE = Decimal(1)
DECIMAL_ONE_HUNDRED = Decimal(100)

# tuples
ALL_OUTPUT_FORMATS = (EXTENSION_JPG, EXTENSION_PNG, EXTENSION_WEBP)
ALL_QUALITIES = (KEYWORD_DEFAULT, QUALITY_COLOR, QUALITY_GRAY, QUALITY_BITONAL)
COLOR_QUALITIES = (QUALITY_BITONAL, QUALITY_COLOR, QUALITY_GRAY)
QUALITY_BITONAL_QUALITIES = (QUALITY_BITONAL,)
QUALITY_GROUP_GRAY = (QUALITY_BITONAL, QUALITY_GRAY)

MEDIA_TYPE_MAPPING = {
    EXTENSION_JPG : MEDIA_TYPE_JPG,
    EXTENSION_PNG : MEDIA_TYPE_PNG,
    EXTENSION_WEBP : MEDIA_TYPE_WEBP
}
