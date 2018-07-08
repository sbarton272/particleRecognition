from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import glob
import os
import numpy as np
from ast import literal_eval


####################################
# Subfunctions for initializing, file opening, and interactions
####################################

def init(data):
    data.circleCenters = [ ]
    data.radii = [ ]
    data.labels = [ ]
    data.imageSize = []

def getFiles(root):
    directory = filedialog.askdirectory()
    root.update()
    name = "."
    path = directory + "/*.png"
    txtpath = directory + "/*.txt"
    files = []
    txtfiles = []
    for fname in glob.glob(path):
        files.append(fname)
    for filename in glob.glob(txtpath):
        txtfiles.append(filename)

    return(files, txtfiles, directory)

def txt_reader(file):
    txt_info = open(file,'r')
    txt = []
    centers = []
    radii = []
    labels = []
    for line in txt_info:
        if line == '\n':
            pass
        else:
            line = line.strip('\n')
            txt.append(line)
    if 'Weird' in txt[0].split(' '):
        weird = txt[0]
    else:
        weird = 'Not Weird Data'
    weird_stop = txt.index('Particle Location:')
    center_stop = txt.index('Radius Size:')
    radius_stop = txt.index('Defect Label:')
    defect_stop = txt.index('Image Size:')
    for loc in txt[weird_stop+1:center_stop]:
        centers.append(literal_eval(loc))
    for loc in txt[center_stop+1:radius_stop] :
        radii.append(int(loc))
    for loc in txt[radius_stop+1:defect_stop]:
        labels.append(loc)
    return(centers, radii,labels, weird)

def imageOpen(files,data):
    image = Image.open(files[data.fileCounter])
    data.imageSize.append(image.size)
    photo = ImageTk.PhotoImage(image)
    imgname = files[data.fileCounter].split('/')[-1].split('.')[0]
    if imgname in data.textnames:
        txtfile = data.directory+'/'+imgname+'.txt'
        centers, radii, labels, weird = txt_reader(txtfile)
    else:
        centers = []
        radii = []
        labels = []
        weird = 'Not Weird Data'
    return(photo, centers, radii, labels, weird)

def saveLabel(files,data):
    split = files[data.fileCounter].split(".")
    fname = split[0] + ".txt"
    label_file = open(fname, "w")
    if data.weird == 'Weird Data':
        label_file.write('Weird Data'+ '\n')
    else:
        label_file.write('Not Weird Data'+ '\n')
    label_file.write("Particle Location:\n")
    for loc in data.circleCenters:
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
    data.newCircleCenter = [float(event.x),event.y+y_offset]
    data.circleCenters.append(data.newCircleCenter)
    data.radii.append(data.radius)
    data.labels.append('null') #this marks particle as found but not atomic rez

def keyPressed(event, data,files,root):
    if (event.keysym == "BackSpace"):
        if (len(data.circleCenters) > 0):
            data.circleCenters.pop()
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
    if event.keysym == "Down": #move circle down
        data.newCircleCenter[1] += 1
        data.circleCenters.pop()
        data.circleCenters.append(data.newCircleCenter)
    if event.keysym == "w":
        if data.weird == 'Weird Data':
            data.weird = 'Not Weird Data'
            print('Marked image not weird')
        else:
            data.weird = 'Weird Data'
            print('Marked image as weird')
    if event.keysym == "Left": #move circle left
        data.newCircleCenter[0] -= 1
        data.circleCenters.pop()
        data.circleCenters.append(data.newCircleCenter)
    if event.keysym == "Right":
        data.newCircleCenter[0] += 1
        data.circleCenters.pop()
        data.circleCenters.append(data.newCircleCenter)
    if (event.char == "y"): #this means there is a stacking fault
        data.labels.pop()
        data.labels.append('yes')
    if (event.char == "n"): #means the particle contained no stacking faults and was atomic rez
        data.labels.pop()
        data.labels.append('no')
    if (event.char == "o"): #this marks particle as found but not atomic rez for use if accidently marked
        data.labels.pop()
        data.labels.append('null')
    if (event.char == "c"): #this means there is a stacking fault on the edge
        data.labels.pop()
        data.labels.append('surfaceSF')
    if (event.char == "f"): #this means there is an edge dislocation
        data.labels.pop()
        data.labels.append('edgeDislcn')
    if event.keysym == "bracketright":
        data.fileCounter += 1
        if data.fileCounter == len(files):
            print('No more images to look at!')
            quitGui(root)
        else:
            data.circleCenters = [ ]
            data.radii = [ ]
            data.labels = [ ]
            data.imageSize = []
            data.photo, data.circleCenters, data.radii, data.labels, data.weird = imageOpen(files,data)
            root.title(files[data.fileCounter])
    if event.keysym == "bracketleft":
        data.fileCounter -= 1
        data.circleCenters = [ ]
        data.radii = [ ]
        data.labels = [ ]
        data.imageSize = []
        data.photo, data.circleCenters, data.radii, data.labels, data.weird = imageOpen(files,data)
        root.title(files[data.fileCounter])
    if event.keysym == "Return":
        saveLabel(files,data)
        data.fileCounter += 1
        if data.fileCounter == len(files):
            print('No more images to look at!')
            quitGui(root)
        else:
            data.circleCenters = [ ]
            data.radii = [ ]
            data.labels = [ ]
            data.imageSize = []
            data.photo, data.circleCenters, data.radii, data.labels, data.weird = imageOpen(files,data)
            root.title(files[data.fileCounter])
            txtpath = data.directory + "/*.txt"
            txtfiles = glob.glob(txtpath)
            data.textFilesCounter = len(txtfiles)
            data.textnames = [name.split('/')[-1].split('.')[0] for name in txtfiles]
    if (event.char == "q"):
        quitGui(root)
def shiftEKeyPressed(event, data,files,root):
    data.radius += 20
    data.radii.pop()
    data.radii.append(data.radius)

def shiftDKeyPressed(event, data,files,root):
    data.radius -= 20
    data.radii.pop()
    data.radii.append(data.radius)


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
    if data.weird == 'Weird Data':
        canvas.create_text(5, data.height-10, activefill = None, fill = 'magenta', font = ('Helvetica', '20','bold'), text = 'W')

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
    def shiftEKeyPressedWrapper(event, canvas, data,root):
        shiftEKeyPressed(event, data,files,root)
        redrawAllWrapper(canvas, data)
    def shiftDKeyPressedWrapper(event, canvas, data,root):
        shiftDKeyPressed(event, data,files,root)
        redrawAllWrapper(canvas, data)
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
    files, textfiles, data.directory = getFiles(root)
    data.textFilesCounter = len(textfiles)
    data.textnames = [name.split('/')[-1].split('.')[0] for name in textfiles]
    data.photo, data.circleCenters, data.radii, data.labels, data.weird = imageOpen(files,data)
    root.title(files[data.fileCounter])
    data.width = 1024
    data.height = 1024
    data.weird = 'not weird'

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
    root.bind("<Shift-Up>", lambda event:
                            shiftEKeyPressedWrapper(event, canvas, data,root))
    root.bind("<Shift-Down>", lambda event:
                            shiftDKeyPressedWrapper(event, canvas, data,root))
    root.bind_all("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data,files,root))

    if data.fileCounter < len(files):
        redrawAll(canvas, data)
        root.mainloop()
    else:
        pass

    # and launch the app
    #root.mainloop()  # blocks until window is closed
    print("bye!")
    print(data.circleCenters,data.radii, data.labels)

run()
