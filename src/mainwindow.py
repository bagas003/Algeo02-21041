from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from tkinter import filedialog
import os

def ressemen():
    print("Button Clicked")

#=================================================================#
def cfile():
        global disphoto

        filename = filedialog.askopenfilename()
        head, tail = os.path.split(filename)
        canvas.itemconfig(NoFilC, text = tail)

        # Load image
        imeg = Image.open(filename)
        resized = imeg.resize((256,256), Image.ANTIALIAS)
        new = ImageTk.PhotoImage(resized)
        
        disphoto = canvas.create_image(541,387,image=new)
        disphoto.tkraise()
#=================================================================#
def cfolder():
        root = Tk()
        root.withdraw()
        folder = filedialog.askdirectory() 
        folder_only = os.path.basename(folder)
        canvas.itemconfig(NoFolC ,text = folder_only)

        # Load image in folder
        '''array_image.clear()
        for matrix in baca_folder(folder):
            array_image.append(matrix)
        print(f"{len(array_image)} pictures loaded, first element:")
        mattest = np.array(array_image[0])
        print(f"Size: {mattest.shape}")
        print(mattest)'''
#=================================================================#

window = Tk()
window.geometry("1280x720")
window.configure(bg = "#FFFFFF")
window.title("Face Recognition")
window.resizable(False, False)

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

bg_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    640.0, 360.0,
    image=bg_img)

img0 = PhotoImage(file = f"btnstart.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = ressemen,
    relief = "flat")
b0.place(
    x = 15, y = 592,
    width = 287,
    height = 105)

img1 = PhotoImage(file = f"btncfile.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = cfile,
    relief = "flat")
b1.place(
    x = 68, y = 450,
    width = 186,
    height = 63)

img2 = PhotoImage(file = f"btncfolder.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = cfolder,
    relief = "flat")
b2.place(
    x = 59, y = 168,
    width = 204,
    height = 64)

NoFolC = canvas.create_text(90,242,
                            text="No Folder Chosen",
                            fill="#FFFFFF",
                            justify="left",
                            anchor="w",
                            font=("Poppins", 12, "bold"))
NoFilC = canvas.create_text(100,523,
                            text="No File Chosen",
                            fill="#FFFFFF",
                            justify="left",
                            anchor="w",
                            font=("Poppins", 12, "bold"))

window.mainloop()