# TinyWP
Lightweight alternative to Wasatch.PY

This project is experimental, and may not be fully functional for all devices. See [Wasatch.PY](https://github.com/WasatchPhotonics/Wasatch.PY), our official driver for most needs. 

```python
import TinyWP
while not TinyWP.get_devices():
    pass
device = TinyWP.get_devices()[0]
TinyWP.init(device)
TinyWP.set_integration_time_ms(device, 1000)
print(TinyWP.get_spectrum(device))
```
