from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import glob
import os
import numpy as np

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
    #image = image.resize((512,512), Image.BICUBIC) #DONT CHANGE THIS UNLESS YOU CHANGE DEPENDECE OF OUTPUT
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
        #real_r = np.multiply(r,2) #because r is with respect to the 512x512 image not 1024x1024
        label_file.write(str(r)+"\n")
    label_file.write("\n"+"Defect Label:"+"\n")
    for label in data.labels:
        label_file.write(label+"\n")
    label_file.write("\n"+"Image Size:"+"\n")
    for size in data.imageSize: #so you can check that the original image was 1024x1024
        label_file.write(str(size)+"\n")
    label_file.close()

def mousePressed(event, data,canvas, scrollbar):
    y_offset = scrollbar.get()[0]*1024
    data.newCircleCenter = [canvas.canvasx(event.x),canvas.canvasy(event.y)+y_offset]
    recordCircleCenter = [canvas.canvasx(event.x),canvas.canvasy(event.y)+y_offset] 
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
        canvas.create_text(center[0], center[1]-(data.radii[idx]+5),activefill = 'magenta',fill = 'black', font = ('Helvetica', '16','bold'),text=data.labels[idx])
    

def quitGui(root):
    root.destroy()
    
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
    redrawAllWrapper(canvas, data)

if __name__ == "__main__":
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, width = 512, height = 512, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = filedialog.askopenfilename(parent=root, initialdir="C:/",title='Choose an image.')
    img = ImageTk.PhotoImage(Image.open(File))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.create_oval(1023, 1023, 1024, 1024, fill="magenta", outline = "magenta")
    canvas.config(scrollregion=canvas.bbox(ALL))
    

    #function to be called when mouse is clicked
    def printcoords(event):
        #outputting x and y coords to console
        x_extra = xscroll.get()
        y_extra = yscroll.get()
        print('x_extra: ', x_extra, 'yextra: ', y_extra)
        print (canvas.canvasx(event.x)+(1024*x_extra[0]),canvas.canvasy(event.y)+(1024*y_extra[0]))
    #mouseclick event
    canvas.bind("<Button 1>",printcoords)

    root.mainloop()