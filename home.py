import ctypes
from Tkinter import *
from tkFileDialog import *
import os
import copy
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter

'''colors'''
very_light_gray = "#989898"
light_gray = "#535353"
medium_gray = "#424242"
dark_gray = "#282828"
text_color = "white"

'''values'''
buttonipady = 10
previousVal = 100
palettePadx = 5
imageWidth = 0
imageHeight = 0
newImageWidth = 1000
newImageHeight = 0
path=""
filename=""

L = []
imageCopy =  Image #stores the copy of the image
image = Image #stores the image opened
displayImage = Image #image currently being displayed

root = Tk()
root.title("Image Editor")
root.state("zoomed")
root.configure(background=dark_gray)
fileLabel = Label(root, text="Import an Image", bg=dark_gray, fg=text_color)
fileLabel.pack(side=TOP)
f1 = Frame(root, width=100, bg=light_gray)
f1.pack(anchor=NW, side=LEFT, fill=BOTH,ipadx=50)
canvas = Canvas(root, width=1000, height=1000, background=very_light_gray)
canvas.pack(anchor=CENTER)

f2 = Frame(root, width=100, bg=light_gray)
f2.pack(anchor=NW, side=RIGHT, fill=BOTH,ipadx=50)

count = -1 #count for undo and redo

def undo(event):
    global count, imageCopy
    count = count - 1
    if(count>=0):
        imageCopy = L[count]
        displayImage = ImageTk.PhotoImage(imageCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
        canvas.mainloop()

def redo(event):
    global count
    count = count + 1
    if(count<len(L)):
        imageCopy = L[count]
        displayImage = ImageTk.PhotoImage(imageCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
        canvas.mainloop()

def display():
    global imageWidth, imageHeight, imageCopy, image, path, filename, displayImage, count, newImageWidth, newImageHeight, size
    filepath = askopenfilename(initialdir="C:\Users\rajbo\Desktop")
    path, filename = os.path.split(filepath)
    fileLabel['text']=filename
    image = Image.open(filepath)
    size = imageWidth, imageHeight = image.size
    newImageWidth = imageWidth
    newImageHeight = imageHeight
    while(newImageWidth>800 or newImageHeight>800):
        newImageWidth = newImageWidth-100
        newImageHeight = newImageWidth * imageHeight / imageWidth
    image = image.resize((newImageWidth, newImageHeight))
    imageCopy = image.copy()
    L.append(copy.deepcopy(imageCopy))
    count += 1
    displayImage = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=displayImage)
    canvas.update()

def saveImage():
    global filename
    s = filename.split(".")
    savefilename = asksaveasfilename(initialdir="C:\Users\rajbo\Desktop", defaultextension=s[1])
    imageCopy.show()
    imageCopy.save(savefilename)

def invertImage():
    global imageCopy, displayImage, count
    imageCopy = ImageOps.invert(imageCopy)
    displayImage = ImageTk.PhotoImage(imageCopy)
    count = count + 1
    L.append(copy.deepcopy(imageCopy))
    canvas.create_image(0, 0, anchor=NW, image=displayImage)
    canvas.update()

def colorImage():
    def temp(event):
        global localCopy
        global imageCopy, displayImage, count, previousVal
        localCopy = imageCopy
        enhancer = ImageEnhance.Color(localCopy)
        localCopy = enhancer.enhance(value.get()+1.0)
        displayImage = ImageTk.PhotoImage(localCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
    def apply():
        global imageCopy, count
        imageCopy = localCopy
        count = count + 1
        L.append(copy.deepcopy(imageCopy))
        master.destroy()
    master = Tk()
    master.title("Color")
    master.config(background=dark_gray)
    value = Scale(master, resolution=0.1, from_=-1.0, to=1.0, orient=HORIZONTAL, bg=dark_gray, fg="white", activebackground=medium_gray, command=temp)
    value.pack(ipadx=40, padx=10, pady=10)
    Button(master, text="Apply",  bg=medium_gray, fg=text_color, command=apply).pack(ipadx=40, padx=10, pady=10)

def brightImage():
    def temp(event):
        global localCopy
        global imageCopy, displayImage, count, previousVal
        localCopy = imageCopy
        enhancer = ImageEnhance.Brightness(localCopy)
        localCopy = enhancer.enhance(value.get()+1.0)
        displayImage = ImageTk.PhotoImage(localCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
    def apply():
        global imageCopy, count
        imageCopy = localCopy
        count = count + 1
        L.append(copy.deepcopy(imageCopy))
        master.destroy()
    master = Tk()
    master.title("Brightness")
    master.config(background=dark_gray)
    value = Scale(master, resolution=0.1, from_=-1.0, to=1.0, orient=HORIZONTAL, bg=dark_gray, fg="white", activebackground=medium_gray, command=temp)
    value.pack(ipadx=40, padx=10, pady=10)
    Button(master, text="Apply",  bg=medium_gray, fg=text_color, command=apply).pack(ipadx=40, padx=10, pady=10)

def contrastImage():
    def temp(event):
        global localCopy
        global imageCopy, displayImage, count, previousVal
        localCopy = imageCopy
        enhancer = ImageEnhance.Contrast(localCopy)
        localCopy = enhancer.enhance(value.get()+1.0)
        displayImage = ImageTk.PhotoImage(localCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
    def apply():
        global imageCopy, count
        imageCopy = localCopy
        count = count + 1
        L.append(copy.deepcopy(imageCopy))
        master.destroy()
    master = Tk()
    master.title("Contrast")
    master.config(background=dark_gray)
    value = Scale(master, resolution=0.1, from_=-1.0, to=1.0, orient=HORIZONTAL, bg=dark_gray, fg="white", activebackground=medium_gray, command=temp)
    value.pack(ipadx=40, padx=10, pady=10)
    Button(master, text="Apply",  bg=medium_gray, fg=text_color, command=apply).pack(ipadx=40, padx=10, pady=10)

def sharpImage():
    def temp(event):
        global localCopy
        global imageCopy, displayImage, count, previousVal
        localCopy = imageCopy
        enhancer = ImageEnhance.Sharpness(localCopy)
        localCopy = enhancer.enhance(value.get()+1.0)
        displayImage = ImageTk.PhotoImage(localCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
    def apply():
        global imageCopy, count
        imageCopy = localCopy
        count = count + 1
        L.append(copy.deepcopy(imageCopy))
        master.destroy()
    master = Tk()
    master.title("Sharpness")
    master.config(background=dark_gray)
    value = Scale(master, resolution=0.1, from_=-2.0, to=2.0, orient=HORIZONTAL, bg=dark_gray, fg="white", activebackground=medium_gray, command=temp)
    value.pack(ipadx=40, padx=10, pady=10)
    Button(master, text="Apply",  bg=medium_gray, fg=text_color, command=apply).pack(ipadx=40, padx=10, pady=10)

def duotoneImage():
    def temp(bid):
        global localCopy
        global imageCopy, displayImage, count, previousVal, alphaValue
        localCopy = imageCopy
        if bid==1:
            duo = Image.new("RGB", (newImageWidth, newImageHeight), "red")
        elif bid==2:
            duo = Image.new("RGB", (newImageWidth, newImageHeight), "blue")
        elif bid==3:
            duo = Image.new("RGB", (newImageWidth, newImageHeight), "green")
        elif bid==4:
            duo = Image.new("RGB", (newImageWidth, newImageHeight), "yellow")
        elif bid==5:
            duo = Image.new("RGB", (newImageWidth, newImageHeight), "aqua")
        elif bid==6:
            duo = Image.new("RGB", (newImageWidth, newImageHeight), "purple")
        elif bid==7:
            duo = Image.new("RGB", (newImageWidth, newImageHeight), "teal")
        elif bid==8:
            duo = Image.new("RGB", (newImageWidth, newImageHeight), "orange")
        localCopy = Image.blend(localCopy, duo, alphaValue)
        displayImage = ImageTk.PhotoImage(localCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
    def temp2(event):
        global alphaValue
        alphaValue = value.get()

    def apply():
        global imageCopy, count
        imageCopy = localCopy
        count = count + 1
        L.append(copy.deepcopy(imageCopy))
        master.destroy()
    master = Tk()
    master.title("Duotone")
    master.config(background=dark_gray)
    value = Scale(master, resolution=0.05, from_=0, to=1.0, orient=HORIZONTAL, bg=dark_gray, fg="white",
                  activebackground=medium_gray, command=temp2)
    value.set(0.2)
    value.pack(ipadx=40, padx=10, pady=10)
    duoFrame = Frame(master)
    Button(duoFrame, bg="red", command=lambda: temp(1)).grid(row=0, column=0, ipadx=palettePadx)
    Button(duoFrame, bg="blue", command=lambda: temp(2)).grid(row=0, column=1, ipadx=palettePadx)
    Button(duoFrame, bg="green", command=lambda: temp(3)).grid(row=0, column=2, ipadx=palettePadx)
    Button(duoFrame, bg="yellow", command=lambda: temp(4)).grid(row=0, column=3, ipadx=palettePadx)
    Button(duoFrame, bg="aqua", command=lambda: temp(5)).grid(row=1, column=0, ipadx=palettePadx)
    Button(duoFrame, bg="purple", command=lambda: temp(6)).grid(row=1, column=1, ipadx=palettePadx)
    Button(duoFrame, bg="teal", command=lambda: temp(7)).grid(row=1, column=2, ipadx=palettePadx)
    Button(duoFrame, bg="orange", command=lambda: temp(8)).grid(row=1, column=3, ipadx=palettePadx)
    duoFrame.pack()
    Button(master, text="Apply", bg=medium_gray, fg=text_color, command=apply).pack(ipadx=40, padx=10, pady=10, side=BOTTOM)

def mirrorImage():
    global imageCopy, displayImage, count
    imageCopy = ImageOps.mirror(imageCopy)
    displayImage = ImageTk.PhotoImage(imageCopy)
    count = count + 1
    L.append(copy.deepcopy(imageCopy))
    canvas.create_image(0, 0, anchor=NW, image=displayImage)
    canvas.update()

def flipImage():
    global imageCopy, displayImage, count
    imageCopy = ImageOps.flip(imageCopy)
    count = count + 1
    L.append(copy.deepcopy(imageCopy))
    displayImage = ImageTk.PhotoImage(imageCopy)
    canvas.create_image(0, 0, anchor=NW, image=displayImage)
    canvas.update()

def resetImage():
    global imageCopy, displayImage, count
    imageCopy = image
    count = count + 1
    L.append(copy.deepcopy(imageCopy))
    displayImage = ImageTk.PhotoImage(imageCopy)
    canvas.create_image(0, 0, anchor=NW, image=displayImage)
    canvas.update()

def grayscaleImage():
    global imageCopy, displayImage, count
    imageCopy = ImageOps.grayscale(imageCopy)
    count = count + 1
    L.append(copy.deepcopy(imageCopy))
    displayImage = ImageTk.PhotoImage(imageCopy)
    canvas.create_image(0, 0, anchor=NW, image=displayImage)
    canvas.update()

def posterImage():
    def temp(event):
        global localCopy
        global imageCopy, displayImage, count, previousVal
        localCopy = imageCopy
        localCopy = ImageOps.posterize(localCopy, value.get())
        displayImage = ImageTk.PhotoImage(localCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
    def apply():
        global imageCopy, count
        imageCopy = localCopy
        count = count + 1
        L.append(copy.deepcopy(imageCopy))
        master.destroy()
    master = Tk()
    master.title("Bit")
    master.config(background=dark_gray)
    value = Scale(master, resolution=1, from_=0, to=8, orient=HORIZONTAL, bg=dark_gray, fg="white", activebackground=medium_gray, command=temp)
    value.set(3)
    value.pack(ipadx=40, padx=10, pady=10)
    Button(master, text="Apply",  bg=medium_gray, fg=text_color, command=apply).pack(ipadx=40, padx=10, pady=10)

def solarImage():
    def temp(event):
        global localCopy
        global imageCopy, displayImage, count, previousVal
        localCopy = imageCopy
        localCopy = ImageOps.solarize(localCopy, value.get())
        displayImage = ImageTk.PhotoImage(localCopy)
        canvas.create_image(0, 0, anchor=NW, image=displayImage)
        canvas.update()
    def apply():
        global imageCopy, count
        imageCopy = localCopy
        count = count + 1
        L.append(copy.deepcopy(imageCopy))
        master.destroy()
    master = Tk()
    master.title("Thresold")
    master.config(background=dark_gray)
    value = Scale(master, resolution=1, from_=0, to=250, orient=HORIZONTAL, bg=dark_gray, fg="white", activebackground=medium_gray, command=temp)
    value.pack(ipadx=40, padx=10, pady=10)
    Button(master, text="Apply",  bg=medium_gray, fg=text_color, command=apply).pack(ipadx=40, padx=10, pady=10)

def autoContrastImage():
    global imageCopy, displayImage, count
    imageCopy = ImageOps.autocontrast(imageCopy)
    count = count + 1
    L.append(copy.deepcopy(imageCopy))
    displayImage = ImageTk.PhotoImage(imageCopy)
    canvas.create_image(0, 0, anchor=NW, image=displayImage)
    canvas.update()

def setWallpaper():
    global imageCopy
    SPI_SETDESKWALLPAPER = 20
    newLocation = "C:/Users/rajbo/Desktop"+filename
    imageCopy.save(newLocation)
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, str(newLocation), 0)

def filterImage(filterId):
    global imageCopy, displayImage, count
    if(filterId==1):
        imageCopy = imageCopy.filter(ImageFilter.BLUR)
    elif(filterId==2):
        imageCopy = imageCopy.filter(ImageFilter.GaussianBlur)
    elif(filterId==3):
        imageCopy = imageCopy.filter(ImageFilter.CONTOUR)
    elif(filterId==4):
        imageCopy = imageCopy.filter(ImageFilter.EDGE_ENHANCE_MORE)
    elif(filterId==5):
        imageCopy = imageCopy.filter(ImageFilter.SHARPEN)
    elif (filterId == 6):
        imageCopy = imageCopy.filter(ImageFilter.SMOOTH_MORE)
    displayImage = ImageTk.PhotoImage(imageCopy)
    count = count + 1
    L.append(copy.deepcopy(imageCopy))
    canvas.create_image(0, 0, anchor=NW, image=displayImage)
    canvas.update()

menubar = Menu(root, bg=medium_gray, fg=text_color, activebackground=dark_gray)
'''file menu'''
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=display)
filemenu.add_command(label="Save", command=saveImage)
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.config(bg=medium_gray, fg=text_color, activebackground=dark_gray)
'''edit menu'''
editmenu = Menu(root, tearoff=0)
editmenu.add_command(label="undo", command=lambda : undo(1), accelerator = 'ctrl+z')
editmenu.add_command(label="redo", command=lambda :redo(2), accelerator = 'ctrl+d')
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.config(bg=medium_gray, fg=text_color, activebackground=dark_gray)
'''image menu'''
imageMenu = Menu(root, tearoff=0)
imageMenu.add_command(label="Invert", command=invertImage)
imageMenu.add_command(label="Grayscale", command=grayscaleImage)
imageMenu.add_command(label="Posterize", command=posterImage)
imageMenu.add_command(label="Solarize", command=solarImage)
imageMenu.add_command(label="Auto Contrast", command=autoContrastImage)
imageMenu.add_command(label="set wallpaper", command=setWallpaper)
menubar.add_cascade(label="Image", menu=imageMenu)
imageMenu.config(bg=medium_gray, fg=text_color, activebackground=dark_gray)
'''filter menu'''
filterMenu = Menu(root, tearoff=0)
filterMenu.add_command(label="Blur", command=lambda: filterImage(1))
filterMenu.add_command(label="Gaussian Blur", command=lambda: filterImage(2))
filterMenu.add_command(label="Contour", command=lambda: filterImage(3))
filterMenu.add_command(label="Edge enhance", command=lambda: filterImage(4))
filterMenu.add_command(label="sharpen", command=lambda: filterImage(5))
filterMenu.add_command(label="smooth", command=lambda: filterImage(6))
menubar.add_cascade(label="Filter", menu=filterMenu)
filterMenu.config(bg=medium_gray, fg=text_color, activebackground=dark_gray)

root.config(menu=menubar)

colorButton = Button(f1, text="Color", command=colorImage, bg=medium_gray, fg=text_color)
colorButton.pack(fill=BOTH, ipady=buttonipady)

brightButton = Button(f1, text="Brightness", command=brightImage, bg=medium_gray, fg=text_color)
brightButton.pack(fill=BOTH, ipady=buttonipady)

contrastButton = Button(f1, text="Contrast", command=contrastImage, bg=medium_gray, fg=text_color)
contrastButton.pack(fill=BOTH, ipady=buttonipady)

sharpButton = Button(f1, text="Sharpness", command=sharpImage, bg=medium_gray, fg=text_color)
sharpButton.pack(fill=BOTH, ipady=buttonipady)

duotoneButton = Button(f1, text="Duotone", command=duotoneImage, bg=medium_gray, fg=text_color)
duotoneButton.pack(fill=BOTH, ipady=buttonipady)

mirrorButton = Button(f1, text="Mirror", command=mirrorImage, bg=medium_gray, fg=text_color)
mirrorButton.pack(fill=BOTH, ipady=buttonipady)

flipButton = Button(f1, text="Flip", command=flipImage, bg=medium_gray, fg=text_color)
flipButton.pack(fill=BOTH, ipady=buttonipady)

resetButton = Button(f1, text="Reset", command=resetImage, bg=medium_gray, fg=text_color)
resetButton.pack(fill=BOTH, ipady=buttonipady)
root.bind_all('<Control-Key-z>', undo)
root.bind_all('<Control-Key-d>', redo)
root.mainloop()