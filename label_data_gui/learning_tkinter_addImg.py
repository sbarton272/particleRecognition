# Basic Animation Framework

from tkinter import *
from PIL import Image, ImageTk


####################################
# customize these functions
####################################

# Adds shapes on mouse clicks and deletes them on pressing 'd'
def init(data):
    data.circleCenters = [ ]
    data.recordCircleCenters = [ ]
    data.radii = [ ]

def mousePressed(event, data,canvas):
    newCircleCenter = (event.x, event.y)
    recordCircleCenter = (canvas.canvasx(event.x),canvas.canvasy(event.y))
    data.circleCenters.append(newCircleCenter)
    data.recordCircleCenters.append(recordCircleCenter)
    data.radii.append(data.radius)

def keyPressed(event, data):
    if (event.char == "d"):
        if (len(data.circleCenters) > 0):
            data.circleCenters.pop(0)
        else:
            print("No more circles to delete!")
    if event.keysym == "Up":
        data.radius += 2
        data.radii.pop()
        data.radii.append(data.radius)
    if event.keysym == "Down":
        data.radius -= 2
        data.radii.pop()
        data.radii.append(data.radius)

def redrawAll(canvas, data,photo):
    #draw the photo
    canvas.create_image(0,0,image = photo,anchor = "nw")
    # draw the circles
    for idx,circleCenter in enumerate(data.circleCenters):
        (cx, cy) = circleCenter
        canvas.create_oval(cx-data.radii[idx], cy-data.radii[idx], cx+data.radii[idx], cy+data.radii[idx], fill=None, outline = "magenta")
    # draw the text
    canvas.create_text(data.width/2, 20,
                       text="Example: Adding and Deleting Shapes")
    canvas.create_text(data.width/2, 40,
                       text="Mouse clicks create circles")
    canvas.create_text(data.width/2, 60,
                       text="Pressing 'd' deletes circles")

####################################
# use the run function as-is
####################################

def run(width=524, height=524):
    def redrawAllWrapper(canvas, data,photo):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data, photo)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data, canvas)
        redrawAllWrapper(canvas, data, photo)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data,photo)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.radius = 20
    data
    root = Tk()
    init(data)
    image = Image.open('/Users/kategroschner/Box Sync/Research/HR-TEM/20180227/20180227_101729F_prepped20171204/8bit/20180227_101729F_plasma15sec_Mh370kx__0014.tif')
    image = image.resize((512,512), Image.BICUBIC)
    photo = ImageTk.PhotoImage(image)
    #label = Label(image=photo)
    #label.image = photo
    #label.pack()
    # create the root and the canvas
    canvas = Canvas(width=data.width, height=data.height)
    canvas.create_image(0,0,image = photo, anchor = "nw")
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data, photo)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
    print(data.recordCircleCenters,data.radii)

run(524, 524)