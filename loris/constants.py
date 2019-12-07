from decimal import Decimal

# strings
BASE_URI_REDIRECT = 'baseUriRedirect'
BITONAL = 'bitonal'
CANONICAL_LINK_HEADER = 'canonicalLinkHeader'
COLOR = 'color'
COMPLIANCE_PAGE = 'http://iiif.io/api/image/3.1/compliance/#compliance'
CONTEXT = 'http://iiif.io/api/image/3/context.json'
CORS = 'cors'
DEFAULT = 'default'
FULL = 'full'
GRAY = 'gray'
HEIGHT = 'height'
IMAGE_SERVICE_3 = 'ImageService3'
JPG = 'jpg'
JPG_MEDIA_TYPE = 'image/jpeg'
JSONLD_MEDIA_TYPE = 'jsonldMediaType'
MAX = 'max'
MAX_AREA = 'maxArea'
MAX_HEIGHT = 'maxHeight'
MAX_WIDTH = 'maxWidth'
PNG = 'png'
PNG_MEDIA_TYPE = 'image/png'
PROFILE_LINK_HEADER = 'profileLinkHeader'
PROTOCOL = 'http://iiif.io/api/image'
REGION_BY_PCT = 'regionByPct'
REGION_BY_PIXEL = 'regionByPx'
REGION_SQUARE = 'regionSquare'
ROTATION_ARBITRARY = 'rotationArbitrary'
ROTATION_BY_90S = 'rotationBy90s'
ROTATION_MIRRORING = 'mirroring'
SCALE_FACTORS = 'scaleFactors'
SIZE_ABOVE_FULL = 'sizeAboveFull'
SIZE_BY_CONFINED_WH = 'sizeByConfinedWh'
SIZE_BY_H = 'sizeByH'
SIZE_BY_PCT = 'sizeByPct'
SIZE_BY_W = 'sizeByW'
SIZE_BY_WH = 'sizeByWh'
SQUARE = 'square'
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
