import json

file = open("st7789v2/conf/font.json")  # noqa: SIM115, PTH123
sinclair = json.loads(file.read())


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


def assemble_string(*characters):
    """Assemble characters into horizontal strings."""
    string = []
    for i in range(len(characters[0])):
        string.append([])
        for character in characters:
            string[-1] += character[i]

    return string


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


def flatten(lists):
    """Flatten some lists."""
    starter = lists[0][0]
    lists[0] = lists[0][1:]
    for lst in lists:
        for item in lst:
            yield (starter, item)
            starter = item


def run_length_encode(data):
    """RLE a list."""
    # we can only send a byte at a time
    max_repeat = 254
    accumulator = 0
    current = None

    for pair in data:
        current = pair[0]
        nxt = pair[1]

        if nxt == current:
            accumulator += 1

        else:
            yield accumulator + 1
            yield current
            accumulator = 0
            current = nxt

        if accumulator > max_repeat:
            yield accumulator
            yield current
            accumulator = 0
            current = nxt

    yield accumulator + 1
    yield current


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
