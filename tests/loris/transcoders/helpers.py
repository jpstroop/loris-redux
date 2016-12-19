GREEN = (0, 150, 0)
RED = (150, 0, 0)
BLUE = (0, 0, 150)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
DARK_SLATE = (49, 79, 79)
BLACK = (0 ,0 ,0)
WHITE = (255 ,255 ,255)

def is_close_color(src_rgb, expected_rgb, threshold=1):
    # Try to account for variations in color that result from compression
    pairs = map(sorted, zip(src_rgb, expected_rgb))
    return all(d <= threshold for d in map(lambda t: t[1]-t[0], pairs))
