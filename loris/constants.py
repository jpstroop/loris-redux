from decimal import Decimal

# strings
ACCEPT_HEADER = 'accept'
ACCESS_CONTROL_ALLOW_HEADERS_HEADER = 'access-control-allow-headers'
ACCESS_CONTROL_ALLOW_METHODS_HEADER = 'access-control-allow-method'
ACCESS_CONTROL_ALLOW_ORIGIN_HEADER = 'access-control-allow-origin'
ACCESS_CONTROL_MAX_AGE_HEADER = 'access-control-max-age'
ALLOW_HEADER = 'allow'
BASE_URI_REDIRECT = 'baseUriRedirect'
BITONAL = 'bitonal'
CANONICAL_LINK_HEADER = 'canonicalLinkHeader'
COLOR = 'color'
COMPLIANCE_PAGE = 'http://iiif.io/api/image/3.1/compliance/#compliance'
CONTENT_TYPE_HEADER = 'content-type'
CONTEXT = '@context'
CONTEXT_URI = 'http://iiif.io/api/image/3/context.json'
CONNECTION_HEADER = "connection"
CORS = 'cors'
DEFAULT = 'default'
EXTRA_FEATURES = 'extraFeatures'
EXTRA_FORMATS = 'extraFormats'
EXTRA_QUALITIES = 'extraQualities'
FULL = 'full'
GRAY = 'gray'
HEIGHT = 'height'
ID = 'id'
IMAGE_SERVICE_3 = 'ImageService3'
JPG = 'jpg'
JPG_MEDIA_TYPE = 'image/jpeg'
JSON_CONTENT_TYPE = 'application/json'
JSONLD_CONTENT_TYPE = 'application/ld+json;profile="http://iiif.io/api/image/3/context.json"'
JSONLD_MEDIA_TYPE = 'jsonldMediaType'
KEEP_ALIVE_HEADER = 'keep-alive'
MAX = 'max'
MAX_AREA = 'maxArea'
MAX_HEIGHT = 'maxHeight'
MAX_WIDTH = 'maxWidth'
PNG = 'png'
PNG_MEDIA_TYPE = 'image/png'
PREFERRED_FORMATS = 'preferredFormats'
PROFILE = 'profile'
PROFILE_LINK_HEADER = 'profileLinkHeader'
PROTOCOL = 'protocol'
PROTOCOL_URI = 'http://iiif.io/api/image'
REGION_BY_PCT = 'regionByPct'
REGION_BY_PIXEL = 'regionByPx'
REGION_SQUARE = 'regionSquare'
ROTATION_ARBITRARY = 'rotationArbitrary'
ROTATION_BY_90S = 'rotationBy90s'
ROTATION_MIRRORING = 'mirroring'
SCALE_FACTORS = 'scaleFactors'
SIZE_BY_CONFINED_WH = 'sizeByConfinedWh'
SIZE_BY_H = 'sizeByH'
SIZE_BY_PCT = 'sizeByPct'
SIZE_BY_W = 'sizeByW'
SIZE_BY_WH = 'sizeByWh'
SIZE_UPSCALING = 'sizeUpscaling'
SIZES = 'sizes'
SQUARE = 'square'
TILES = 'tiles'
TYPE = 'type'
VARY_HEADER = 'vary'
WEBP = 'webp'
WEBP_MEDIA_TYPE = 'image/webp'
WIDTH = 'width'

# numbers and objects
DECIMAL_ONE = Decimal(1)
DECIMAL_ONE_HUNDRED = Decimal(100)

# tuples
ALL_OUTPUT_FORMATS = (JPG, PNG, WEBP)
ALL_QUALITIES = (DEFAULT, COLOR, GRAY, BITONAL)
BITONAL_QUALITIES = (BITONAL,)
COLOR_QUALITIES = (BITONAL, COLOR, GRAY)
GRAY_QUALITIES = (BITONAL, GRAY)

MEDIA_TYPE_MAPPING = {
    JPG : JPG_MEDIA_TYPE,
    PNG : PNG_MEDIA_TYPE,
    WEBP : WEBP_MEDIA_TYPE
}
