from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window2 = Tk()

#Key down functions
def click():
    circle_radius = textentry.get()

#Put in photo
image = Image.open('/Users/kategroschner/Box Sync/Research/HR-TEM/20180227/20180227_101729F_prepped20171204/8bit/20180227_101729F_plasma15sec_Mh370kx__0012.tif')
photo = ImageTk.PhotoImage(image)
label = Label(window, image = photo).grid(row = 0, column = 0,sticky = W)

#Second window with menus
label2 = Label(window2, text = "Enter radius of circle:", font = "none 12 bold")\
.grid(row = 0, column = 0, sticky = W)
textentry = Entry(window2,width = 20, bg = "blue")
textentry.grid(row = 1, column = 0, sticky = W)
Button(window2, text = "Submit", width = 6, command = click).grid(row = 3, \
column = 0, sticky = W)



#run mainloop 
window.mainloop()
window2.mainloop()
