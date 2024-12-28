from lib.screen_tools import (
    horizontal_centering_offsets,
    rgb_to_332,
    vertical_centering_offsets,
)


def test_rgb_to_332():
    """Test we can convert colours."""
    assert rgb_to_332((255, 255, 255)) == 255  # noqa: PLR2004
    assert rgb_to_332((0, 0, 0)) == 0
    assert rgb_to_332((225, 0, 0)) == 224  # noqa: PLR2004
    assert rgb_to_332((0, 225, 0)) == 28  # noqa: PLR2004
    assert rgb_to_332((0, 0, 255)) == 3  # noqa: PLR2004


def test_horizontal_centering_offsets():
    """Test we can centre text horizontally."""
    assert horizontal_centering_offsets("a", 1) == [116, 123]
    assert horizontal_centering_offsets("123", 2) == [96, 143]


def test_vertical_centering_offsets():
    """Test we can centre text vertically."""
    assert vertical_centering_offsets(1) == [63, 70]
    assert vertical_centering_offsets(4) == [51, 82]
