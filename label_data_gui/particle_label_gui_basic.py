# Basic Animation Framework

from tkinter import *
from PIL import Image, ImageTk
import glob
import os


####################################
# customize these functions
####################################

# Adds shapes on mouse clicks and deletes them on pressing 'd'
def init(data):
    data.circleCenters = [ ]
    data.recordCircleCenters = [ ]
    data.radii = [ ]
    data.labels = [ ]

def getFiles():
    try:
        path = "/Users/kategroschner/Box Sync/Research/HR-TEM/20180227/20180227_101729F_prepped20171204/8bit"    
        
        name = "."
        length1 = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        
    except:
        path = "/Users/cgroschner/Box Sync/Research/HR-TEM/20180227/20180227_101729F_prepped20171204/8bit"    
    
        name = "."
        length1 = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        

    path = path + "/*.tif"    
    files = []
    for fname in glob.glob(path):
        files.append(fname)
    
    return(files, path)

def imageOpen(files,data):
    image = Image.open(files[data.fileCounter])
    image = image.resize((512,512), Image.BICUBIC) #DONT CHANGE THIS UNLESS YOU CHANGE DEPENDECE OF OUTPUT
    photo = ImageTk.PhotoImage(image)
    return(photo)
    
def saveLabel(files,data):
    split = files[data.fileCounter].split(".")
    fname = split[0] + ".txt"
    label_file = open(fname, "w")
    label_file.write("Particle Location:\n")
    for loc in data.recordCircleCenters:
        label_file.write(str(loc)+"\n")
    label_file.write("\n"+"Radius Size:"+"\n")
    for r in data.radii:
        label_file.write(str(r)+"\n")
    label_file.write("\n"+"Defect Label:"+"\n")
    for label in data.labels:
        label_file.write(label+"\n")
    label_file.close()

def mousePressed(event, data,canvas):
    newCircleCenter = (event.x, event.y)
    recordCircleCenter = [canvas.canvasx(event.x)*2,canvas.canvasy(event.y)*2] #NOTE THE TIMES TWO
    data.circleCenters.append(newCircleCenter)
    data.recordCircleCenters.append(recordCircleCenter)
    data.radii.append(data.radius)
    data.labels.append('null') #this marks particle as found but not atomic rez

def keyPressed(event, data,files,root):
    if (event.char == "d"):
        if (len(data.circleCenters) > 0):
            data.circleCenters.pop()
            data.recordCircleCenters.pop()
            data.radii.pop()
            data.labels.pop()
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
    if (event.char == "y"): #this means there is a stacking fault
        data.labels.pop()
        data.labels.append('yes')
    if (event.char == "n"): #means the particle contained no stacking faults and was atomic rez
        data.labels.pop()
        data.labels.append('no')
    if event.keysym == "Return":
        saveLabel(files,data)
        data.fileCounter += 1
        data.photo = imageOpen(files,data)
        data.circleCenters = [ ]
        data.recordCircleCenters = [ ]
        data.radii = [ ]
        data.labels = [ ]
    if (event.char == "q"):
        quitGui(root)

def redrawAll(canvas, data):
    #draw the photo
    canvas.create_image(0,0,image = data.photo,anchor = "nw")
    # draw the circles
    for idx,circleCenter in enumerate(data.circleCenters):
        if (len(data.radii) > 0):
            (cx, cy) = circleCenter
            canvas.create_oval(cx-data.radii[idx], cy-data.radii[idx], cx+data.radii[idx], cy+data.radii[idx], fill=None, outline = "magenta")
        else:
            (cx, cy) = circleCenter
            canvas.create_oval(cx-data.radii[idx], cy-data.radii[idx], cx+data.radius, cy+data.radius, fill=None, outline = "magenta")
    # draw the text
    canvas.create_text(data.width/2, 20,
                       text="Example: Adding and Deleting Shapes")
    canvas.create_text(data.width/2, 40,
                       text="Mouse clicks create circles")
    canvas.create_text(data.width/2, 60,
                       text="Pressing 'd' deletes circles")

def quitGui(root):
    root.destroy()
####################################
# use the run function as-is
####################################

def run(width=524, height=524):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data, canvas)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas,data,files,root):
        keyPressed(event, data,files,root)
        redrawAllWrapper(canvas, data)
    
    files = getFiles()[0]
    
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.radius = 20
    data.fileCounter = 0
    data
    root = Tk()
    init(data)
    data.photo = imageOpen(files,data)
    #get first image to label
    #files = getFiles()
    #image = Image.open(files[0])
    #image = image.resize((512,512), Image.BICUBIC) #DONT CHANGE THIS
    #photo = ImageTk.PhotoImage(image)

    # create the root and the canvas
    canvas = Canvas(width=data.width, height=data.height)
    canvas.create_image(0,0,image = data.photo, anchor = "nw")
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data,files,root))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")
    print(data.recordCircleCenters,data.radii, data.labels)

run(524, 524)