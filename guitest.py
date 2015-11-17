#!/usr/bin/env python
# coding: utf-8

import Tkinter
from PIL import Image, ImageTk

root = Tkinter.Tk()
frame = Tkinter.Frame(root)
image = Image.open("sample1_back.jpeg")
tkpi = ImageTk.PhotoImage(image)
label_image = Tkinter.Label(frame, image=tkpi)
label_image.pack()
frame.pack()
root.mainloop()