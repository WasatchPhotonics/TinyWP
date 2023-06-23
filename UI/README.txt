Considering different UI libraries.

Priorities:

1. simple dependency situation
2. performant arbitrary rendering

Synopsis

test_window_Pyside2.py
- works
- redirects to PySide6... Does not seem like a future proof solution.
- known to push breaking changes, causes version issues since revisions need platform specific builds -- this is the problem with bindings. A non-stable API creates a real shitstorm.

test_window_Pyside6.py
- crashes on Ubuntu due to missing backend

test_window_PySimpleGUI.py
- works
- does not seem to have full windowing events: resize, move
- supports arbitrary rendering

test_window_tkinter.py
- works
