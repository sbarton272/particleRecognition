from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import glob
import os
import numpy as np


####################################
# Subfunctions for initializing, file opening, and interactions
####################################

def init(data):
    data.circleCenters = [ ]
    data.recordCircleCenters = [ ]
    data.radii = [ ]
    data.labels = [ ]
    data.newCircleCenter = [0,0]
    data.imageSize = []

def getFiles(root):
    directory = filedialog.askdirectory() 
    root.update()  
    name = "."
    path = directory + "/*.png"
    print(path)    
    files = []
    for fname in glob.glob(path):
        files.append(fname)
    
    return(files, path)

def imageOpen(files,data):
    image = Image.open(files[data.fileCounter])
    data.imageSize.append(image.size)
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
    label_file.write("\n"+"Image Size:"+"\n")
    for size in data.imageSize: 
        label_file.write(str(size)+"\n")
    label_file.close()

def mousePressed(event, data,canvas, scrollbar):
    y_offset = scrollbar.get()[0]*1024
    data.newCircleCenter = [event.x,event.y+y_offset] 
    recordCircleCenter = [float(event.x),event.y+y_offset] 
    data.circleCenters.append(data.newCircleCenter)
    data.recordCircleCenters.append(recordCircleCenter)
    data.radii.append(data.radius)
    data.labels.append('null') #this marks particle as found but not atomic rez

def keyPressed(event, data,files,root):
    if (event.keysym == "BackSpace"):
        if (len(data.circleCenters) > 0):
            data.circleCenters.pop()
            data.recordCircleCenters.pop()
            data.radii.pop()
            data.labels.pop()
        else:
            print("No more circles to delete!")
    if event.char == "e": #enlarge circle
        data.radius += 1
        data.radii.pop()
        data.radii.append(data.radius)
    if event.char == "d": #decrease circle
        data.radius -= 1
        data.radii.pop()
        data.radii.append(data.radius)
    if event.keysym == "Up": #move circle up
        data.newCircleCenter[1] -= 1
        data.circleCenters.pop()
        data.circleCenters.append(data.newCircleCenter)
        data.recordCircleCenters[-1][1] -= 1
    if event.keysym == "Down": #move circle down
        data.newCircleCenter[1] += 1
        data.circleCenters.pop()
        data.circleCenters.append(data.newCircleCenter)
        data.recordCircleCenters[-1][1] += 1
    if event.keysym == "Left": #move circle left
        data.newCircleCenter[0] -= 1
        data.circleCenters.pop()
        data.circleCenters.append(data.newCircleCenter)
        data.recordCircleCenters[-1][0] -= 1
    if event.keysym == "Right":
        data.newCircleCenter[0] += 1
        data.circleCenters.pop()
        data.circleCenters.append(data.newCircleCenter)
        data.recordCircleCenters[-1][0] += 1
    if (event.char == "y"): #this means there is a stacking fault
        data.labels.pop()
        data.labels.append('yes')
    if (event.char == "n"): #means the particle contained no stacking faults and was atomic rez
        data.labels.pop()
        data.labels.append('no')
    if (event.char == "o"): #this marks particle as found but not atomic rez for use if accidently marked
        data.labels.pop()
        data.labels.append('null')
    if event.keysym == "Return":
        saveLabel(files,data)
        data.fileCounter += 1
        if data.fileCounter == len(files):
            print('No more images to look at!')
            quitGui(root)
        else:
            data.photo = imageOpen(files,data)
            data.circleCenters = [ ]
            data.recordCircleCenters = [ ]
            data.radii = [ ]
            data.labels = [ ]
            data.imageSize = []
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
    for idx,center in enumerate(data.circleCenters):
        canvas.create_text(center[0], center[1]-(data.radii[idx]+5),activefill = 'magenta',fill = 'black', font = ('Helvetica', '18','bold'),text=data.labels[idx])
    

def quitGui(root):
    print('Quiting...')
    root.destroy()
###############
#Main Function to run GUI
###############

def run():
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data, scrollbar):
        mousePressed(event, data, canvas, scrollbar)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas,data,files,root):
        keyPressed(event, data,files,root)
        if data.fileCounter < len(files):
            redrawAllWrapper(canvas, data)
        else:
            pass

    # Set up data structure
    class Struct(object): pass
    
    #initialize all the required data
    data = Struct()
    data.radius = 50
    data.fileCounter = 0
    init(data)
    print('shift+click to select particle','\n', 'arrow keys move circle','\n', '"e" enlarges circle, "d" decreases circle', '\n', '"y" to label stacking fault','\n', '"n" to label no visible stacking fault','\n', '"o" if only one plane of particle is resolved','\n', 'hit enter to continue to next image', '\n', '"q" quits program')
    

    #run the main image labeling gui
    root = Tk()
    files = getFiles(root)[0]
    data.photo = imageOpen(files,data)
    data.width = 1024
    data.height = 1024

    # create the root and the canvas
    canvas = Canvas(width=data.width, height=data.height)
    
    
    #Create scrollbar
    scrollbar = Scrollbar(root)
    scrollbar.config(command = canvas.yview)
    scrollbar.pack(side = RIGHT, fill = Y)
    canvas.config(yscrollcommand = scrollbar.set)
    canvas.pack(side = LEFT, expand = True, fill = 'both')
    canvas.create_image(0,0,image = data.photo, anchor = "nw")
    canvas.config(scrollregion = canvas.bbox(ALL))
    
    # set up events
    root.bind("<Shift-Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data,scrollbar))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data,files,root))
    if data.fileCounter < len(files):
        redrawAll(canvas, data) 
        root.mainloop()
    else:
        pass
    
    # and launch the app
    #root.mainloop()  # blocks until window is closed
    print("bye!")
    print(data.recordCircleCenters,data.radii, data.labels)

run()