"""
Enable area scan mode
Set integration time to 1000ms
Acquire spectrum and display it as a 2D area scan heatmap.

TODO rewrite using tkinter for rendering
"""

# --------------------- Begin Imports ---------------------------- #

import TinyWP
from TinyWP import WPPostProc

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
window.title("Area Scan")
canvas = Canvas(window, width=500, height=500)
canvas.pack()

FPS = 60

# ---------------------   End Window Initialization -------------- #
# --------------------- Begin Device Parameters ------------------ #

TinyWP.set_integration_time_ms(device, 16)
TinyWP.set_area_scan(device, 1)
horizontal = TinyWP.get_line_length(device)
vertical = TinyWP.get_active_pixels_vertical(device)

y = 0
# for drawing purposes
row_buffer = [None,] * horizontal * vertical

# ---------------------   End Device Parameters ------------------ #
# --------------------- Begin Mainloop --------------------------- #

def update():
    """
    Draw one row of pixels from area scan per frame

    framerate is 60fps and there are ~64 rows
    areascan fully updates once per second
    """

    global y

    # get spectrum
    spectrum = TinyWP.get_spectrum(device)
    # _ contains the row index reported from the device,
    # but this was unreliable when I tried it
    _, spectrum = spectrum[0], [spectrum[1]]+spectrum[1:]

    # use tkinter canvas to draw area scan
    for x in range(len(spectrum)):
        #color(int(255*spectrum[x]/max(spectrum)), 0, 0, 255)
        #vertex(10+x, 10+y)

        # TODO: delete rectangles that are drawn over
        gObj = row_buffer[y*horizontal+x]
        if gObj:
            canvas.delete(gObj)

        # create persistent graphics objects for each row of areascan
        hi = max(spectrum)
        lo = min(spectrum)
        # per row saturation adjustment
        v = int(255 * (spectrum[x]-lo)/(hi-lo))
        color = f'#{hex(v)[2:].zfill(2)}0000'
        row_buffer[y*horizontal+x] = canvas.create_rectangle(x, y, x+1, y+1, fill=color, outline='')

    y += 1
    y %= vertical

    window.after(1000//FPS, update)

window.after(1000//FPS, update)

window.mainloop()

# ---------------------   End Mainloop --------------------------- #
