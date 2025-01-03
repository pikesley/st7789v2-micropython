from st7789v2.lib.screen_tools import (
    horizontal_centering_offsets,
    vertical_centering_offsets,
)


def test_horizontal_centering_offsets():
    """Test we can centre text horizontally."""
    assert horizontal_centering_offsets("a", 1) == [116, 123]
    assert horizontal_centering_offsets("123", 2) == [96, 143]


def test_vertical_centering_offsets():
    """Test we can centre text vertically."""
    assert vertical_centering_offsets(1) == [63, 70]
    assert vertical_centering_offsets(4) == [51, 82]
