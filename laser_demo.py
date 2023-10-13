"""
Turn the laser on and off, with user input
(doesn't work)
"""

import TinyWP

print("Waiting for device...")
while not TinyWP.get_devices():
    pass
device = TinyWP.get_devices()[0]

print("Found Wasatch Device.", type(device))
TinyWP.init(device)

input("Press [ENTER] to power on laser.")
TinyWP.set_laser_power_perc(device, 20)

input("Press [ENTER] to power off laser.")
TinyWP.set_laser_power_perc(device, 0)
