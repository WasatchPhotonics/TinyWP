Considering different UI libraries.

Priorities:

1. simple dependency situation
2. performant arbitrary rendering

Out of box support matrix

             Ubuntu 22   macOS 13.2.1  Windows 11
PySide2        YES*         NO          PARTIAL -- required conda env downgrade to 3.10
PySide6        NO          YES          YES
tkinter**      YES         YES          YES
PySimpleGUI    YES         YES          YES
 
*downgrade to py37 on Ubuntu had to do with Enlighten-specific implementation details
**tkinter (and therefore PySimpleGUI) are pretty much guranteed to run consistently on every platform

Synopsis - (Ubuntu only)

test_window_Pyside2.py
- works
- redirects to PySide6... Does not seem like a future proof solution.
- known to push breaking changes, causes version issues since revisions need platform specific builds -- this is the problem with bindings. A non-stable API creates a real problem.

test_window_Pyside6.py
- crashes on Ubuntu due to missing backend

test_window_PySimpleGUI.py
- works
- does not seem to have full windowing events: resize, move
- supports arbitrary rendering

test_window_tkinter.py
- works
- supports arbitrary rendering

see docs: https://www.tcl.tk/man/
https://docs.python.org/3/library/tk.html
