"""
Enable area scan mode
Set integration time to 1000ms
Acquire spectrum and display it as a 2D area scan heatmap.

This implementation is written using OpenGL 3.0.

Only windows is supported, because that's where `pip install pyglet`
is sufficient to cover all GL dependencies.

On other platforms, it is possible to run, but additional dynamic library 
dependencies may need to be installed.
"""

import pyglet
from pyglet.gl import *

import TinyWP

import sys
import time

FPS = 60

print("Waiting for device...")
while not TinyWP.get_devices():
    pass
device = TinyWP.get_devices()[0]
print("Found Wasatch Device.", type(device))
TinyWP.init(device)
TinyWP.set_area_scan(device, 1)
start = time.time()

window = pyglet.window.Window(resizable=True)

TinyWP.set_integration_time_ms(device, 100)

vertical = TinyWP.get_active_pixels_vertical(device)

y = 0

#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_SRC_ALPHA)

@window.event
def on_key_press(symbol, modifiers):
    window.clear()

@window.event
def on_mouse_motion(x, y, dx, dy):
    pass

def on_draw(*k):
    global y

    # capture full image each frame (set to 1 for single row)
    rows_per_frame = vertical

    for i in range(rows_per_frame):
        # get spectrum
        spectrum = TinyWP.get_spectrum(device)
        # _ contains the row index reported from the device, but this was unreliable when I tried it
        _, spectrum = spectrum[0], [spectrum[1]]+spectrum[1:]

        # use pyglet GL to draw area scan
        glBegin(GL_POINTS)
        for x in range(len(spectrum)):

            # adapting exposure
            lo = min(spectrum)
            hi = max(spectrum)

            # low exposure
            #lo = 0
            #hi = 14000

            v = (spectrum[x]-lo)/(hi-lo)
            glColor4f(v, 0, 0, 1)
            glVertex2f(10+x+.5, 10+y+.5)
        glEnd()

        y += 1
        y %= vertical

pyglet.clock.schedule_interval(on_draw, 1./FPS)
pyglet.app.run()

