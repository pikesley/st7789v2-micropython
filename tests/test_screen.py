from unittest.mock import MagicMock, call

from lib.screen import ST7789v2


def test_initialisation():
    """Test screen initialises."""
    mocked_i2c = MagicMock()
    _ = ST7789v2(i2c=mocked_i2c)

    assert mocked_i2c.mock_calls == [
        call.writeto_mem(62, 34, bytearray([255])),
        call.writeto_mem(62, 32, bytearray([0])),
        call.writeto_mem(62, 54, bytearray([1])),
        call.writeto_mem(62, 105, bytearray([0, 0, 240, 135, 0])),
    ]


def test_different_starting_background():
    """Test we can start with a different colour."""
    mocked_i2c = MagicMock()
    _ = ST7789v2(i2c=mocked_i2c, background_colour=(255, 0, 0))

    assert mocked_i2c.mock_calls[-1] == call.writeto_mem(
        62, 105, bytearray([0, 0, 240, 135, 224])
    )


def test_clearing_screen():
    """Test we can clear the screen."""
    mocked_i2c = MagicMock()
    st = ST7789v2(i2c=mocked_i2c, background_colour=(255, 0, 0))
    st.clear_screen()

    assert mocked_i2c.mock_calls[-1] == call.writeto_mem(
        62, 105, bytearray([0, 0, 240, 135, 224])
    )


def test_clearing_screen_with_a_different_colour():
    """Test we clear the screen wth a different colour."""
    mocked_i2c = MagicMock()
    st = ST7789v2(i2c=mocked_i2c, background_colour=(255, 0, 0))
    st.clear_screen()

    assert mocked_i2c.mock_calls[-1] == call.writeto_mem(
        62, 105, bytearray([0, 0, 240, 135, 224])
    )

    st.clear_screen((0, 255, 0))
    assert mocked_i2c.mock_calls[-1] == call.writeto_mem(
        62, 105, bytearray([0, 0, 240, 135, 28])
    )

    assert st.background_colour == (0, 255, 0)


def test_writing_text():
    """Test we can write text."""
    mocked_i2c = MagicMock()
    st = ST7789v2(i2c=mocked_i2c, background_colour=(255, 0, 0))

    st.write_text("A", x=0, y=0, colour=(0, 255, 0), scale_factor=1)

    assert mocked_i2c.mock_calls[-3] == call.writeto_mem(62, 42, bytearray([0, 7]))
    assert mocked_i2c.mock_calls[-2] == call.writeto_mem(62, 43, bytearray([0, 7]))
    assert mocked_i2c.mock_calls[-1] == call.writeto_mem(
        62,
        65,
        bytearray(
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                28,
                28,
                28,
                28,
                0,
                0,
                0,
                28,
                0,
                0,
                0,
                0,
                28,
                0,
                0,
                28,
                0,
                0,
                0,
                0,
                28,
                0,
                0,
                28,
                28,
                28,
                28,
                28,
                28,
                0,
                0,
                28,
                0,
                0,
                0,
                0,
                28,
                0,
                0,
                28,
                0,
                0,
                0,
                0,
                28,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
            ]
        ),
    )


def test_writing_centered_text():
    """Test we can write centered text."""
    mocked_i2c = MagicMock()
    st = ST7789v2(i2c=mocked_i2c, background_colour=(255, 0, 0))

    st.write_text("A", x="centered", y="centered", colour=(0, 0, 255), scale_factor=4)

    assert mocked_i2c.mock_calls[-3] == call.writeto_mem(62, 42, bytearray([104, 135]))
    assert mocked_i2c.mock_calls[-2] == call.writeto_mem(62, 43, bytearray([51, 82]))
