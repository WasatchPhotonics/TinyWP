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

# @window.event
def on_draw(*k):
    window.clear()

    # get spectrum
    spectrum = TinyWP.get_spectrum(device)
    y, spectrum = spectrum[0], [spectrum[1]]+spectrum[1:]

    print(y)

    # use pyglet GL to draw area scan
    glBegin(GL_POINTS)
    for x in range(200):
        for y in range(20):
            glColor4f(200, 0, 200, 255)
            glVertex2f(10+x, 10+y)
    glEnd()

pyglet.clock.schedule_interval(on_draw, 1/60.)
pyglet.app.run()

