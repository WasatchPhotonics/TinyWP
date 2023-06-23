from tkinter import *
root = Tk()
root.geometry("500x500")
canvas = Canvas(root, width=500, height=500)
canvas.pack()
# png = PhotoImage(file = r'example.png') # Just an example
# canvas.create_image(0, 0, image = png, anchor = "nw")

a = canvas.create_rectangle(10, 10, 100, 100, fill='red')
canvas.move(a, 20, 20)

canvas.create_text(20, 20, text="Hello")

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
