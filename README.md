# TinyWP
Lightweight alternative to Wasatch.PY

```python
import TinyWP
while not TinyWP.get_devices():
    pass
device = TinyWP.get_devices()[0]
TinyWP.init(device)
TinyWP.set_integration_time_ms(device, 1000)
print(TinyWP.get_spectrum(device))
```

Should I implement this in ANSI C?
