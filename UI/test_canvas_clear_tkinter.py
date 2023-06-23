"""
This is another demo of realtime rendering in tkinter canvas using a different approach
"""

from tkinter import *

# create window
root = Tk()
root.geometry("500x500")

# create rendering context
canvas = Canvas(root, width=500, height=500)
canvas.pack()

FPS = 60

x, y = 10, 10

def update():

    # clear canvas
    canvas.delete("all")

    global x, y, r

    x += 1
    color = f'#{hex(x % 0xff)[2:].zfill(2)}0000'

    # due to clear, this is like an immediate-mode function
    r = canvas.create_rectangle(x, y, 100+x, 100+y, fill=color, outline='')

    root.after(1000//FPS, update)


# `after` is a language feature from Tcl. 
#
# In Python it is attached to the Tk() instance, and it is used like this:
# 
#       timer = root.after(ms, callback)
#
# `ms` is the amount of time in milliseconds before `callback` should be called.
# `timer` keeps track of the request, which can be cancelled later:
#
#       root.after_cancel(timer)
root.after(1000//FPS, update)

# enter Tk/Tcl mainloop
root.mainloop()
