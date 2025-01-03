from st7789v2.lib.colour_tools import rgb_to_332


def test_rgb_to_332():
    """Test we can convert colours."""
    assert rgb_to_332((255, 255, 255)) == 255  # noqa: PLR2004
    assert rgb_to_332((0, 0, 0)) == 0
    assert rgb_to_332((225, 0, 0)) == 224  # noqa: PLR2004
    assert rgb_to_332((0, 225, 0)) == 28  # noqa: PLR2004
    assert rgb_to_332((0, 0, 255)) == 3  # noqa: PLR2004
