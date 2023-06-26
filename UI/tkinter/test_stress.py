from tkinter import *
root = Tk()
root.geometry("1000x1000")
canvas = Canvas(root, width=1000, height=1000)
canvas.pack()

for x in range(1000):
    for y in range(1000):
        u, v, w, h = 10+x, 10+y, 1, 1
        a = canvas.create_rectangle(u, v, u+w, v+h, fill=f'#{hex(x%256)[2:].zfill(2)}0000', outline="")

canvas.create_text(120, 20, text="Hello")

# 1M draws in 6sec on Ubuntu 22.04 in VMWare

"""
create_arc
create_bitmap
create_image
create_line
create_oval
create_polygon
create_rectangle
create_text
"""

root.mainloop()
