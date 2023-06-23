"""
Enable area scan mode
Set integration time to 1000ms
Acquire spectrum and display it as a 2D area scan heatmap.

Partial implementation.
"""

import pyglet
from pyglet.gl import *

import sys
import TinyWP
import WPPostProc
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

import time

print("Waiting for device...")
while not TinyWP.get_devices():
    pass
device = TinyWP.get_devices()[0]
print("Found Wasatch Device.", type(device))
TinyWP.init(device)
window = pyglet.window.Window(resizable=True)
start = time.time()

TinyWP.set_integration_time_ms(device, 16)
TinyWP.set_area_scan(device, 1)

vertical = TinyWP.get_active_pixels_vertical(device)

y = 0

# @window.event
def on_draw(*k):
    # window.clear()

    # get spectrum
    spectrum = TinyWP.get_spectrum(device)
    # _ contains the row index reported from the device, but this was unreliable when I tried it
    _, spectrum = spectrum[0], [spectrum[1]]+spectrum[1:]

    # use pyglet GL to draw area scan
    glBegin(GL_POINTS)
    for x in range(200):
        for y in range(20):
            glColor4f(int(255*spectrum[x]/max(spectrum)), 0, 0, 255)
            glVertex2f(10+x, 10+y)
    glEnd()

    y += 1
    y %= vertical

pyglet.clock.schedule_interval(on_draw, 1/60.)
pyglet.app.run()
