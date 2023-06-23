"""
Enable area scan mode
Set integration time to 1000ms
Acquire spectrum and display it as a 2D area scan heatmap.

TODO rewrite using tkinter for rendering
"""

# --------------------- Begin Imports ---------------------------- #

import TinyWP
import WPPostProc

from tkinter import *
from tkinter import ttk

import time
import sys

# ---------------------   End Imports ---------------------------- #
# --------------------- Begin Device Connection ------------------ #

print("Waiting for device...")
while not TinyWP.get_devices():
    pass
device = TinyWP.get_devices()[0]
print("Found Wasatch Device.", type(device))
TinyWP.init(device)

# ---------------------   End Device Connection ------------------ #
# --------------------- Begin Window Initialization -------------- #

window = Tk()
frame = ttk.Frame(window, padding=10)
frame.grid()

start = time.time()

# ---------------------   End Window Initialization -------------- #
# --------------------- Begin Device Parameters ------------------ #

TinyWP.set_integration_time_ms(device, 16)
TinyWP.set_area_scan(device, 1)
vertical = TinyWP.get_active_pixels_vertical(device)

y = 0

# ---------------------   End Device Parameters ------------------ #
# --------------------- Begin Mainloop --------------------------- #

def update():

    # get spectrum
    spectrum = TinyWP.get_spectrum(device)
    # _ contains the row index reported from the device,
    # but this was unreliable when I tried it
    _, spectrum = spectrum[0], [spectrum[1]]+spectrum[1:]

    # use tkinter canvas to draw area scan
    for x in range(200):
        for y in range(20):
            pass
            #color(int(255*spectrum[x]/max(spectrum)), 0, 0, 255)
            #vertex(10+x, 10+y)

    y += 1
    y %= vertical

window.mainloop()

# ---------------------   End Mainloop --------------------------- #
