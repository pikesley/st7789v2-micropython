import os

from st7789v2.conf.conf import (
    brightness,
    colours,
    device,
    invert_colours,
    pins,
    rotation_type,
    size,
)
from st7789v2.lib.colour_tools import reduce_colour
from st7789v2.lib.font_tools import text_data
from st7789v2.lib.screen_tools import (
    horizontal_centering_offsets,
    vertical_centering_offsets,
)

if os.uname().sysname == "esp32":
    from machine import Pin, SoftI2C

    i2c = SoftI2C(sda=Pin(pins["sda"]), scl=Pin(pins["scl"]), freq=400000)


class ST7789v2:
    """LCD screen."""

    def __init__(
        self,
        i2c,
        background_colour=colours["background"],
    ):
        """Construct."""
        self.i2c = i2c
        self.device = device
        self.background_colour = background_colour

        self.turn_on()
        self.set_inversion()
        self.rotate()
        self.clear()

    def turn_on(self):
        """Turn screen on."""
        self.send_command(0x22, brightness)

    def rotate(self, rotation_type=rotation_type):
        """Rotate screen."""
        self.send_command(0x36, rotation_type)

    def set_inversion(self):
        """Set colour inversion."""
        command = 0x20
        if invert_colours:
            command = 0x21

        self.send_command(command, 0)

    def clear(self, colour=None):
        """Start again."""
        if colour:
            self.background_colour = colour

        self.fill_screen(self.background_colour)

    def fill_screen(self, colour):
        """Fill the screen with colour."""
        self.draw_rect(0, 0, size["x"], size["y"], colour)

    def draw_rect(self, x_left, y_top, x_right, y_bottom, colour):
        """Draw a rectangle."""
        colour = reduce_colour(colour)
        self.send_command(0x69, [x_left, y_top, x_right, y_bottom, colour])

    def send_command(self, command, data):
        """Send a command."""
        if not isinstance(data, list):
            data = [data]

        try:  # noqa: SIM105
            self.i2c.writeto_mem(self.device, command, bytearray(data))
        except OSError:
            pass

    def write_text(self, text, colour, x="centered", y="centered", scale_factor=2):
        """Write the text at (x, y)."""
        offset = scale_factor * 8
        colour = reduce_colour(colour)

        x_offsets = (
            horizontal_centering_offsets(text, scale_factor)
            if x == "centered"
            else [x, x + (offset * len(text)) - 1]
        )

        y_offsets = (
            vertical_centering_offsets(scale_factor)
            if y == "centered"
            else [y, y + offset - 1]
        )

        self.send_command(0x2A, x_offsets)
        self.send_command(0x2B, y_offsets)

        command = 0x49
        data = text_data(text, scale_factor=scale_factor, on_colour=colour, rle=True)

        buffer = []
        for byte in data:
            buffer.append(byte)
            if len(buffer) > 4095:  # noqa: PLR2004
                print("flushing")
                self.send_command(command, buffer)
                buffer = []

        self.send_command(command, buffer)


if os.uname().sysname == "esp32":
    screen = ST7789v2(i2c=i2c)
