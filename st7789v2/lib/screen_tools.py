from st7789v2.conf.conf import size


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
