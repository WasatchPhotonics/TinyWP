import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import TinyWP
print("Waiting for device...")
while not TinyWP.get_devices():
    pass
device = TinyWP.get_devices()[0]
print("Found Wasatch Device.", type(device))
TinyWP.init(device)
TinyWP.set_integration_time_ms(device, 100)

spectrum = TinyWP.get_spectrum(device)

class Scope:
    def __init__(self, ax, maxt=2):
        self.ax = ax

        self.line = Line2D([], [])
        self.ax.add_line(self.line)

        self.ax.set_xlim(0, len(spectrum))
        self.ax.set_ylim(min(spectrum), max(spectrum))

    def update(self, t):
        #self.ax.figure.canvas.draw()

        spectrum = TinyWP.get_spectrum(device)
        self.line.set_data(range(len(spectrum)), spectrum)
        return self.line,


def emitter(p=0.1):
    """Return a random value in [0, 1) with probability p, else 0."""
    while True:
        v = np.random.rand()
        if v > p:
            yield 0.
        else:
            yield np.random.rand()


# Fixing random state for reproducibility
np.random.seed(19680801 // 10)


fig, ax = plt.subplots()
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, emitter, interval=50,
                              blit=True, save_count=100)

plt.show()
