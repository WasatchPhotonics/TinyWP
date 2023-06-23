from tkinter import *

# create window
root = Tk()
root.geometry("500x500")

# create rendering context
canvas = Canvas(root, width=500, height=500)
canvas.pack()

FPS = 60

x, y = 10, 10

# initialize drawing object
r = canvas.create_rectangle(x, y, 100+x, 100+y, fill='red', outline='')

def update():
    global x, y, r

    x += 1

    # change coordinates over time
    #canvas.coords(r, x, y, 100+x, 100+y)

    # change color over time
    canvas.itemconfig(r, fill=f'#{hex(x % 0xff)[2:].zfill(2)}0000') 

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
