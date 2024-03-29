"""
Set integration time to 1000ms
Acquire spectrum
Print output to terminal
"""
import TinyWP
print("Waiting for device...")
while not TinyWP.get_devices():
    pass
device = TinyWP.get_devices()[0]
print("Found Wasatch Device.", type(device))
TinyWP.init(device)
TinyWP.set_integration_time_ms(device, 1000)
print(TinyWP.get_spectrum(device))
