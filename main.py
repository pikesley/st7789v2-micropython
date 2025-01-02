import gc
import secrets
import time

import micropython
import network
import ntptime

from screen import screen, size

scale_factor = 4
separators = [":", " "]
text = "© 1982 Sinclair Research Ltd."
clock_colour = 0xF0
banner_colour = 0x1C
profile = False


def connect():
    """Connect to wifi."""
    wlan = network.WLAN(network.WLAN.IF_STA)
    wlan.active(True)  # noqa: FBT003
    wlan.connect(secrets.SSID, secrets.KEY)


def sync():
    """Sync the clock."""
    ntptime.settime()


def write_banner():
    """Write the important text."""
    screen.write_text(
        text,
        x="centered",
        y=size["y"] - 16,
        colour=banner_colour,
        scale_factor=1,
    )


def get_time(separator):
    """Get the time string."""
    now = time.localtime()
    return f"{now[3]:02}{separator}{now[4]:02}"


def rotate(array):
    """Rotate the array."""
    return [array[-1]] + array[:-1]


def write_time(separator):
    """Write the time."""
    screen.write_text(
        get_time(separator),
        x="centered",
        y="centered",
        colour=clock_colour,
        scale_factor=scale_factor,
    )

    gc.collect()
    time.sleep(0.5)

    if profile:
        micropython.mem_info()


if __name__ == "__main__":
    screen.clear()
    write_banner()
    connect()
    time.sleep(3)
    sync()

    while True:
        write_time(separators[0])
        separators = rotate(separators)
