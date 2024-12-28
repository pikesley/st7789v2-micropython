import json
import os
from math import floor

if os.uname().sysname == "esp32":
    from machine import Pin, SoftI2C

    i2c = SoftI2C(sda=Pin(9), scl=Pin(8), freq=400000)


size = {"x": 240, "y": 135}

device = 0x3E

font_path = "conf/font.json"
if os.uname().sysname == "esp32":
    font_path = "screen/conf/font.json"

file = open(font_path)  # noqa: SIM115, PTH123
sinclair = json.loads(file.read())


class ST7789v2:
    """LCD screen."""

    def __init__(
        self,
        i2c,
        device=device,
        background_colour=0,
        brightness=255,
        invert_colours=False,  # noqa: FBT002
    ):
        """Construct."""
        self.i2c = i2c
        self.device = device
        self.background_colour = background_colour
        self.brightness = brightness
        self.invert_colours = invert_colours

        self.turn_on()
        self.set_inversion()
        self.rotate()
        self.clear_screen()

    def turn_on(self):
        """Turn screen on."""
        self.send_command(0x22, self.brightness)

    def rotate(self, rotation_type=1):
        """Rotate screen."""
        self.send_command(0x36, rotation_type)

    def set_inversion(self):
        """Set colour inversion."""
        command = 0x20
        if self.invert_colours:
            command = 0x21

        self.send_command(command, 0)

    def clear_screen(self, colour=None):
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

        self.i2c.writeto_mem(self.device, command, bytearray(data))

    def write_text(self, text, x, y, colour, scale_factor=2):
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

        data = text_data(text, scale_factor=scale_factor, on_colour=colour, rle=False)
        # 0x49 for RLE
        self.send_command(0x41, data)


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


def bytes_to_bits(byte_list):
    """Turn bytes into lists of bits."""
    return [[int(i) for i in list(f"{byte:#010b}"[2:])] for byte in byte_list]


def scale_bits(bits, scale):
    """Scale lists of bits."""
    scaled_bits = []
    for line in bits:
        scaled_bits.append([])
        for bit in line:
            for _ in range(scale):
                scaled_bits[-1].append(bit)

        for _ in range(scale - 1):
            scaled_bits.append(scaled_bits[-1])

    return scaled_bits


def colour_bits(bits, on_colour, off_colour):
    """Apply colours to bits."""
    if isinstance(on_colour, int):
        on_colour = (on_colour,)
    if isinstance(off_colour, int):
        off_colour = (off_colour,)

    coloured_bits = []
    for line in bits:
        coloured_bits.append([])
        for bit in line:
            if bit == 0:
                for element in off_colour:
                    coloured_bits[-1].append(element)
            if bit == 1:
                for element in on_colour:
                    coloured_bits[-1].append(element)

    return coloured_bits


def assemble_string(*characters):
    """Assemble characters into horizontal strings."""
    string = []
    for i in range(len(characters[0])):
        string.append([])
        for character in characters:
            string[-1] += character[i]

    return string


def flatten(lists):
    """Flatten some lists."""
    return sum(lists, [])  # noqa: RUF017


def run_length_encode(data):
    """RLE a list."""
    # TODO: there's a bug here
    encoded = []
    accumulator = 0
    step = 0
    current = data[0]

    for step in range(len(data) - 1):
        current = data[step]
        nxt = data[step + 1]

        if nxt == current:
            accumulator += 1

        else:
            encoded.append(accumulator + 1)
            encoded.append(current)
            accumulator = 0
            current = nxt

    encoded.append(accumulator + 1)
    encoded.append(current)

    return encoded


def text_data(text, scale_factor=2, on_colour=255, off_colour=0, rle=False):  # noqa: FBT002
    """Get some printable data from some ASCII text."""
    characters = [
        scale_bits(bytes_to_bits(sinclair[character]), scale_factor)
        for character in text
    ]

    string = assemble_string(*characters)
    coloured = colour_bits(string, on_colour, off_colour)
    flattened = flatten(coloured)

    if rle:
        return run_length_encode(flattened)

    return flattened


if os.uname().sysname == "esp32":
    screen = ST7789v2(i2c=i2c)
