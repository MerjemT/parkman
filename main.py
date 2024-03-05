import os

import PIL
from PIL import Image, ImageTk
from tkinter import *
from tkinter import filedialog

from PredictCharacters import predict_license_plate_number
from TrainRecognizeCharacters import train
from dbAPI import database

dir_name = 'output'
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
else:
    filelist = [f for f in os.listdir(dir_name) if f.endswith(".png")]
    for f in filelist:
        os.remove(os.path.join(dir_name, f))

if not os.path.exists(os.path.join(__location__, 'finalized_model.sav')):
    train()

def nove_dimenzije(dimenzije, zeljena_sirina=250):
    sirina = dimenzije[0]
    visina = dimenzije[1]
    t = (zeljena_sirina, int((visina / sirina) * zeljena_sirina))
    return t

class photos(Frame):
    def __init__(self, parent, images):
        Frame.__init__(self, parent)
        for i, image in enumerate(images):
            img = PIL.Image.open(f"output/{image}")
            img = img.resize(nove_dimenzije(img.size))
            img = ImageTk.PhotoImage(img)

            self.image = Label(parent, image=img)
            self.image.image = img
            # self.image.pack()
            self.image.grid(column=i%2, row=int(i/2))

class window():
    def __init__(self):
        self.db = database()

        self.root = Tk()
        self.root.title("Parkman")
        self.root.minsize(800,600)

        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=2)
        self.spaceEater = Frame(self.root)
        self.spaceEater.grid(column=1, row=0)

        self.image_upload = Frame(self.root)
        self.lbl1 = Label(self.image_upload, text="Select a photo from which to extract the licence plate", padx=20)
        self.btn1 = Button(self.image_upload, text="Select photo", command=self.clicked)
        self.lbl1.pack(side=LEFT)
        self.btn1.pack(side=LEFT)
        self.image_upload.grid(column=0, row=0)

        self.occupancyRoot = Frame(self.root, padx=10, pady=10)
        self.occupancyRoot.grid_columnconfigure(0, weight=1)
        self.occupancySpaceEater = Frame(self.occupancyRoot)
        self.occupancyLbl = Label(self.occupancyRoot, text="Occupied spaces: ", padx=15)
        self.occupancy = Button(self.occupancyRoot, text="", state=DISABLED, bg="lime green", disabledforeground="black",
        padx=20, pady=10)
        self.occupancySign()
        self.occupancyLbl.pack(side=LEFT)
        self.occupancy.pack()
        self.occupancyRoot.grid(column=2, row=0)

        self.root.mainloop()

    def clicked(self):
        filelist = [f for f in os.listdir('output') if f.endswith(".png")]
        for f in filelist:
            os.remove(os.path.join('output', f))

        file = filedialog.askopenfilename(initialdir=f"{__file__}/samples/", filetypes=(("Picture", ".jpg .png"), ("JPG", ".jpg"), ("PNG", "*.png")))
        plate_string, rightplate_string = predict_license_plate_number(file)
        images = next(os.walk('output'))[2]
        self.imageInfo = Frame(self.root)
        lbl1 = Label(self.imageInfo, text=F"Found characters: {plate_string}")
        lbl2 = Label(self.imageInfo, text=F"Characters in order: {rightplate_string}")
        lbl1.pack()
        lbl2.pack()
        self.imageInfo.grid(column=0, row=1)
        if hasattr(self, "picRoot"):
            self.picRoot.destroy()
        self.picRoot = Frame(self.root)
        pictures = photos(self.picRoot, images)
        pictures.grid()
        self.picRoot.grid(column=0, row=2)

        self.carStatus = Frame(self.root)
        self.lblEnterTime = Label(self.carStatus, text="")
        self.lblExitTime = Label(self.carStatus, text="")
        self.lblTotalTime = Label(self.carStatus, text="")
        self.lblPriceTime = Label(self.carStatus, text="")

        if self.db.isIn(plate_string):
            self.carExiting(plate_string)
        else:
            self.carEntering(plate_string)

        self.lblEnterTime.pack()
        self.lblExitTime.pack()
        self.lblTotalTime.pack()
        self.lblPriceTime.pack()
        self.carStatus.grid(column=2, row=1)
        self.occupancySign()

    def carExiting(self, plate_string):
        entrance_time, exit_time, time_diff = self.db.carExit(plate_string)
        self.lblEnterTime["text"] = "Entrance time: " + str(entrance_time)
        self.lblExitTime["text"] = "Exit time: " + str(exit_time)
        self.lblTotalTime["text"] = "Time parked: " + str(time_diff)
        self.lblPriceTime["text"] = "Total price: $" + str(float(time_diff) * self.db.price)
    def carEntering(self, plate_string):
        entrance_time = self.db.carEnter(plate_string)
        self.lblEnterTime["text"] = "Entrance time: " + str(entrance_time)

    def occupancySign(self):
        occupiedSpaces = self.db.getOccupiedSpacesNo()
        self.occupancy["text"] = str(occupiedSpaces) + "/" + str(self.db.space)
        if occupiedSpaces >= self.db.space:
            self.occupancy["bg"] = "red"
        elif occupiedSpaces > int(2*self.db.space/3):
            self.occupancy["bg"] = "orange"
        elif occupiedSpaces > int(self.db.space/3):
            self.occupancy["bg"] = "yellow"
        else:
            self.occupancy["bg"] = "lime green"
window()