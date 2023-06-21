"""
Set integration time to 1000ms
Continuously acquire spectra and display it in a window
"""

import pyglet

import sys
import TinyWP
from TinyWP import WPPostProc
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

TinyWP.set_integration_time_ms(device, 1000)

@window.event('on_draw')
def on_draw(*k):
    window.clear()

    # get spectrum
    spectrum = WPPostProc.process(lambda: TinyWP.get_spectrum(device))

    # render plot (matplotlib)
    dpi_res = min(window.width, window.height) / 10
    fig = Figure((window.width / dpi_res, window.height / dpi_res), dpi=dpi_res)
    ax = fig.add_subplot(111)
    X = range(len(spectrum))
    Y = spectrum
    ax.plot(X, Y, lw=2, color="k")
    canvas = FigureCanvasAgg(fig)
    data, (w, h) = canvas.print_to_buffer()
    image = pyglet.image.ImageData(w, h, "RGBA", data, -4 * w)

    image.blit(0, 0)

pyglet.app.run()

