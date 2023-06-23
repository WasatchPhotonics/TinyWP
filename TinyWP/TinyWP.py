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
from .DeviceFinderUSB import DeviceFinderUSB

from time import sleep

"""
Constants
"""

HOST_TO_DEVICE = 0x40
DEVICE_TO_HOST = 0xc0

READ_TIMEOUT = 5000 # ms

"""
Utility Functions
"""

def _interleave_lsb_msb(raw_data):
    # Iterate across the received bytes in 'data' as two interleaved arrays.
    # (i) starts at zero (even bytes) and (j) starts at 1 (odd bytes).
    return [int(i | (j << 8)) for i, j in zip(raw_data[::2], raw_data[1::2])] # LSB-MSB

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

    # TODO from ENG-001
    # these are probably defaulted to correct, but that would be undefined behavior
    # LINK_MOD_TO_INTEGRATION = 0
    # MOD_ENABLE = 0
    # SET_TRIGGER_SOURCE = 0

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

def is_FX2(device):
    # specification varies across FX2 and ARM
    # AFAIK, the only way to detect if it's an FX2 is via PID 0x1000, 0x2000 = FX2, 0x4000 = ARM
    raise NotImplementedError()

def get_line_length(device):
    "get number of pixels reported by device"

    # TODO check if EEPROM is involved, if so: mention in docstring

    seq = device.ctrl_transfer(DEVICE_TO_HOST, 0xff, 0x03, 0, 64)
    return seq[1]<<8 + seq[0]

"""
Getters
"""

# TODO do something smart wrt msg_bytes and get_line_length, do not overcook EEPROM
def get_spectrum(device, msg_bytes=1024):
    device.ctrl_transfer(HOST_TO_DEVICE, 0xAD, 0, 0)
    raw_data = device.read(0x82, msg_bytes, READ_TIMEOUT)

    # TODO
    # FX2 with 2048 pixels (4096 byte msg) respond with half on 0x82 and half on 0x86

    return _interleave_lsb_msb(raw_data)

def get_active_pixels_vertical(device):

    # not implemented, hardcoded to match my test XM device
    return 64

def get_area_scan(device, msg_bytes_per_line=1024, line_count=None):
    device.ctrl_transfer(HOST_TO_DEVICE, 0xAD, 0, 0)

    if line_count is None:
        line_count = 1 # get_active_pixels_vertical(device)

    total_msg_bytes = msg_bytes_per_line * line_count
    raw_data = device.read(0x82, total_msg_bytes, READ_TIMEOUT)

    area_scan = []

    for line in range(line_count):
        startIndex = line*msg_bytes_per_line
        endIndex = startIndex+msg_bytes_per_line

        raw_data_line = raw_data[startIndex:endIndex]

        # Iterate across the received bytes in 'data' as two interleaved arrays.
        # (i) starts at zero (even bytes) and (j) starts at 1 (odd bytes).
        interleaved_line = [int(i | (j << 8)) for i, j in zip(raw_data_line[::2], raw_data_line[1::2])] # LSB-MSB

        area_scan.append(interleaved_line)

    return area_scan

def get_spectrum_deferred(*vargs, **kwargs):
    return lambda: get_spectrum(*vargs, **kwargs)

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

def set_area_scan(device, enable=1):
    device.ctrl_transfer(HOST_TO_DEVICE, 0xEB, enable)

