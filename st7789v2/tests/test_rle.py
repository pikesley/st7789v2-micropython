from st7789v2.lib.font_tools import run_length_encode


def fake_flatten(items):
    """Pretend we flattened these."""
    starter = items[0]
    items = items[1:]
    for item in items:
        yield (starter, item)
        starter = item


def test_rle():
    """Test it does run-length encoding."""
    bits = fake_flatten([3, 4])
    assert list(run_length_encode(bits)) == [1, 3, 1, 4]

    bits = fake_flatten([5, 5, 6])
    assert list(run_length_encode(bits)) == [2, 5, 1, 6]

    bits = fake_flatten([0, 4, 4, 0, 0, 6, 6, 6, 0, 0, 1, 0, 2, 2, 0, 0])
    assert list(run_length_encode(bits)) == [
        1,
        0,
        2,
        4,
        2,
        0,
        3,
        6,
        2,
        0,
        1,
        1,
        1,
        0,
        2,
        2,
        2,
        0,
    ]


def test_long_rle():
    """Test it breaks up long rle runs."""
    bits = fake_flatten([0] * 1000 + [3] * 500 + [0, 0])
    assert list(run_length_encode(bits)) == [
        255,
        0,
        255,
        0,
        255,
        0,
        235,
        0,
        255,
        3,
        245,
        3,
        2,
        0,
    ]
