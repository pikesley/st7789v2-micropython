import gc
import secrets
import time

import micropython
import network
import ntptime

from st7789v2.conf.conf import size
from st7789v2.screen import screen

scale_factor = 6
text = "© 1982 Sinclair Research Ltd."
clock_colour = (255, 0, 255)
banner_colour = (0, 255, 255)
tick_interval = 500
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

    if profile:
        micropython.mem_info()


def setup():
    """Initialise."""
    screen.clear()
    write_banner()
    connect()
    time.sleep(3)
    sync()


def tick():
    """Tell the time."""
    separators = [":", " "]

    while True:
        start_ticks = time.ticks_ms()
        write_time(separators[0])
        while (time.ticks_ms() - start_ticks) < tick_interval:
            pass

        if profile:
            print(time.ticks_ms())

        separators = rotate(separators)
