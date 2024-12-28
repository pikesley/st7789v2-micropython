from screen import run_length_encode


def test_rle():
    """Test it does run-length encoding."""
    bits = [2]
    assert run_length_encode(bits) == [1, 2]

    bits = [3, 4]
    assert run_length_encode(bits) == [1, 3, 1, 4]

    bits = [5, 5, 6]
    assert run_length_encode(bits) == [2, 5, 1, 6]

    bits = [0, 4, 4, 0, 0, 6, 6, 6, 0, 0, 1, 0, 2, 2, 0, 0]
    assert run_length_encode(bits) == [
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


def test_log_rle():
    """Test it breaks up long rle runs."""
    bits = [0] * 1000 + [3] * 500 + [0, 0]
    assert run_length_encode(bits) == [
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
