"""
@title TinyWP
@description Lightweight python driver for Wasatch Photonics spectrometers
@author Samie Bee

Lightweight alternative to Wasatch.PY

This module will always be stateless, single-threaded, and immediate.
Only types included in python or pyusb are used.
Error handling is the responsibility of the caller.

Simulation, profiling, and logging may be implemented as replacement modules.
ie `import TinyWPSim` in place of `import TinyWP`

Post-processing should be implemented in parallel as opposed to as a wrapper.
ie DO:
    ```
    import TinyWP
    import WPPostProcess
    # ...
    s = TinyWP.get_spectrum(device)
    print(WPPostProcess.process(s))
    ```
DO NOT:
    ```
    import TinyWPWrapper
    print(TinyWPWrapper.get_spectrum()) # output has post-processing
    ```
"""

import usb
import usb.core
import usb.util
import usb.backend.libusb0 as libusb0

# This is kept from Wasatch.PY for now because of platform-specific branching
from DeviceFinderUSB import DeviceFinderUSB

from time import sleep

"""
Constants
"""

HOST_TO_DEVICE = 0x40
DEVICE_TO_HOST = 0xc0

READ_TIMEOUT = 5000 # ms

"""
Device Mgmt
"""

# returns a list of usb.core.Devices containing all connected Wasatch supported devices
def get_devices():
    device_ids = DeviceFinderUSB().find_usb_devices(poll=True)
    return list(set(device_ids))

# performs initialization steps
def init(device):
    device.set_configuration()
    usb.util.claim_interface(device, 0)

"""
Device Info
"""

def is_arm(device):
    raise NotImplementedError()

def is_imx(device):
    raise NotImplementedError()

def is_imx392(device):
    raise NotImplementedError()

def is_ingaas(device):
    raise NotImplementedError()

def is_micro(device):
    raise NotImplementedError()

def get_line_length(device):
    seq = device.ctrl_transfer(DEVICE_TO_HOST, 0xff, 0x03, 0, 64)
    return seq[1]<<8 + seq[0]

"""
Getters
"""

def get_spectrum(device, msg_bytes=1024):
    device.ctrl_transfer(HOST_TO_DEVICE, 0xAD, 0, 0)
    return device.read(0x82, msg_bytes, READ_TIMEOUT)

def get_wavelengths(device):
    raise NotImplementedError()

def get_wavenumbers(device):
    raise NotImplementedError()

"""
Setters
"""

def set_integration_time_ms(device, integration_time_ms):
    ms = max(1, int(round(integration_time_ms)))
    lsw =  ms        & 0xffff
    msw = (ms >> 16) & 0x00ff
    device.ctrl_transfer(HOST_TO_DEVICE, 0xB2, lsw, msw)