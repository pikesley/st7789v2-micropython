from math import floor

size = {"x": 240, "y": 135}


def rgb_to_332(rgb):
    """Convert a 24-bit (r, g, b) colour to an rgb332 byte."""
    # https://stackoverflow.com/a/25258336
    red = floor(rgb[0] / 32) << 5
    green = floor(rgb[1] / 32) << 2
    blue = floor(rgb[2] / 64)

    return red + green + blue


def horizontal_centering_offsets(text, scale_factor):
    """Provide x-offsets for centred text."""
    width = len(text) * 8 * scale_factor
    left = int((size["x"] - width) / 2)
    right = int(left + width - 1)

    return [left, right]


def vertical_centering_offsets(scale_factor):
    """Provide y-offsets for centred text."""
    offset = 8 * scale_factor
    top = int((size["y"] - offset) / 2)
    bottom = int(top + offset - 1)

    return [top, bottom]


def reduce_colour(rgb):
    """Detect if we're given an RGB triple and replace with an RGB332 byte."""
    if not isinstance(rgb, int):
        rgb = rgb_to_332(rgb)

    return rgb
