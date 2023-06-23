"""
Used for comparison with TinyWP
"""

import pyglet

import sys
sys.path.append("../Wasatch.PY")

from wasatch.WasatchBus    import WasatchBus
from wasatch.WasatchDevice import WasatchDevice
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

bus = WasatchBus()
if not bus.device_ids:
    import sys
    
    print("no spectrometers found")
    sys.exit(1)

device_id = bus.device_ids[0]
print("found %s" % device_id)

device = WasatchDevice(device_id)
if not device.connect():
    print("connection failed")
    sys.exit(1)

print("Found Wasatch Device.", type(device))

window = pyglet.window.Window(resizable=True)

start = time.time()

device.hardware.set_integration_time_ms(1000)

@window.event('on_draw')
def on_draw(*k):
    window.clear()

    # get spectrum
    spectrum = device.hardware.get_line().data.spectrum

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

