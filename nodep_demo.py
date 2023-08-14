#!/usr/bin/env python3

# title nodep_demo.py
# author Samie Bee
# description Demonstrates sending and receiving messages via pyusb without any other dependencies

"""
Key Terms:
  Byte - 8 bits.
  Word - 16 bits.
  Dword - 32 bits.
  LSB - Least Signficant Byte. In 0xAAAABBBB, 0xBBBB is the LSB.
  MSB - Most Significant Byte. In 0xAAAABBBB, 0xAAAA is the MSB.
"""

import usb
import usb.backend.libusb0 as libusb0

HOST_TO_DEVICE = 0x40
DEVICE_TO_HOST = 0xc0
READ_TIMEOUT = 5000 # ms

def get_device():
    """
    Wait for a single Wasatch ARM-based device to be connected, and return the libusb0 object to caller.
    """
    device = None
    while not device:
        device = usb.core.find(idVendor=0x24aa, idProduct=0x4000, backend=libusb0.get_backend())
    return device

def init(device):
    """
    Perform basic device initialization. 
    
    This is not an exhaustive implementation of initialization, but it should be enough to work with during development.
    See TinyWP.py for details about undefined aspects.
    """
    device.set_configuration()
    usb.util.claim_interface(device, 0)

def _interleave_lsb_msb(raw_data):
    """
    Iterate across the received bytes and combine them into words.
    """
    # (i) starts at zero (even bytes) and (j) starts at 1 (odd bytes).
    return [int(i | (j << 8)) for i, j in zip(raw_data[::2], raw_data[1::2])] # LSB-MSB

if __name__=="__main__":
    ### START ###
    print("Waiting for device...")
    device = get_device()
    init(device)
    print("CONNECTED to 0x24aa (Wasatch VID), 0x4000 ARM-based product")
    
    ### SEND A MESSAGE ###
    print("Setting integration time to 500ms.")
    endpoint = 0xB2 # 0xB2 is set integration time
    word = 500 # parameter (milliseconds)
    lsw =  word        & 0xffff # divide dword into separate bytes
    msw = (word >> 16) & 0x00ff
    device.ctrl_transfer(HOST_TO_DEVICE, endpoint, lsw, msw) # send message
    
    ### ACQUIRE SPECTRUM ###
    print("Acqusition request.")
    device.ctrl_transfer(HOST_TO_DEVICE, 0xAD, 0, 0) # 0xAD is an acquire spectrum request
    raw_data = device.read(0x82, msg_bytes, READ_TIMEOUT) # the response comes back on endpoint 0x82
    spectrum = _interleave_lsb_msb(raw_data) # this function combines a sequence of [lsb, msb, lsb, msb, ...] into [word, word, ...]
    print("Received response.")
