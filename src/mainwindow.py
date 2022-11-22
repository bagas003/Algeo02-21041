from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
from main import *
import os

#=================================================================#

def start():
    if new != '' and folderonly != '' :
        # print("Button Clicked")
        global disresult, opres

        closestres, exetime, similari = runprogram(folderdirac, filename)
        print(similari)
        discr = str(folderdirac) + '/' + closestres
        if similari >= 50 :
            if len(closestres) > 17 :
                closestres = closestres[:17]
            canvas.itemconfig(distimeex ,text = str(round(exetime,6)) + 's')
            canvas.itemconfig(fcresult ,text = closestres)
        else :
            discr = "./srcimg/NoFoundPic.png"
            canvas.itemconfig(distimeex ,text = '0s')
            canvas.itemconfig(fcresult ,text = 'No picture found!')

        # print(discr)
        opres = Image.open(discr)
        reszopres = opres.resize((256,256), Image.ANTIALIAS)
        disresult = ImageTk.PhotoImage(reszopres)
        frame2 = Frame(window, width= 256, height= 256)
        frame2.pack()
        frame2.place(x= 787, y= 259, anchor=NW)

        labelres = Label(frame2,image=disresult)
        labelres.pack()

    else :
        messagebox.showerror("Error","Anda belum memilih folder dan file nya!")

#=================================================================#

def cfile():
        global new, imeg
        global filename
        filename = ''
        new = ''

        filename = filedialog.askopenfilename()
        head, tail = os.path.split(filename) # tail = nama file tanpa direct
        
        if tail != '' :
            copytail = tail # Buat display nama file tak lebih dari 22 char.
            if len(copytail) > 22 :
                copytail = copytail[:22]
            canvas.itemconfig(NoFilC, text = copytail)

            # Load image
            imeg = Image.open(filename)
            resized = imeg.resize((256,256), Image.ANTIALIAS)
            new = ImageTk.PhotoImage(resized)
            frame1 = Frame(window, width= 256, height= 256)
            frame1.pack()
            frame1.place(x= 413, y= 259, anchor=NW)

            labeldis = Label(frame1,image=new)
            labeldis.pack()

#=================================================================#

def cfolder(): 
        global folderdirac, folderonly
        folderonly = ''
        folderdirac = ''

        folderdirac = filedialog.askdirectory() 
        # print(folderdirac)
        folderonly = os.path.basename(folderdirac)
        if folderonly != '' :
            copyfolnly = folderonly # Buat display nama folder tak lebih dari 22 char.
            if len(copyfolnly) > 22 :
                copyfolnly = copyfolnly[:22]
            canvas.itemconfig(NoFolC ,text = copyfolnly)

#=================================================================#

window = Tk()
window.geometry("1280x720")
window.configure(bg = "#FFFFFF")
window.title("Face Recognition")
window.resizable(False, False)

ico = Image.open('./srcimg/iconnya.png')
icon = ImageTk.PhotoImage(ico)
window.wm_iconphoto(False, icon)

# Sementara
folderonly = ''
disphoto = ''

canvas = Canvas(window,
        bg = "#FFFFFF",
        height = 720,
        width = 1280,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
canvas.place(x = 0, y = 0)

bg_img = PhotoImage(file = f"./srcimg/background.png")
background = canvas.create_image(
    640.0, 360.0,
    image=bg_img)

img0 = PhotoImage(file = f"./srcimg/btnstart.png")
b0 = Button(image = img0,
        borderwidth = 0,
        highlightthickness = 0,
        command = start,
        relief = "flat")
b0.place(x = 15, y = 592,
        width = 287,
        height = 105)

img1 = PhotoImage(file = f"./srcimg/btncfile.png")
b1 = Button(image = img1,
        borderwidth = 0,
        highlightthickness = 0,
        command = cfile,
        relief = "flat")
b1.place(x = 68, y = 450,
        width = 186,
        height = 63)

img2 = PhotoImage(file = f"./srcimg/btncfolder.png")
b2 = Button(image = img2,
        borderwidth = 0,
        highlightthickness = 0,
        command = cfolder,
        relief = "flat")
b2.place(x = 59, y = 168,
        width = 204,
        height = 64)

NoFolC = canvas.create_text(155,247,
                            text="No Folder Chosen",
                            fill="#FFFFFF",
                            justify="left",
                            anchor="center",
                            font=("Poppins", 12, "bold"))
NoFilC = canvas.create_text(156,525,
                            text="No File Chosen",
                            fill="#FFFFFF",
                            justify="left",
                            anchor="center",
                            font=("Poppins", 12, "bold"))

distimeex = canvas.create_text(572,608, 
                            text= '0s',
                            fill="#FFFFFF",
                            justify="left",
                            anchor="w",
                            font=("Poppins", 12, "bold"))

fcresult = canvas.create_text(871,608, 
                            text= '',
                            fill="#FFFFFF",
                            justify="left",
                            anchor="w",
                            font=("Poppins", 12, "bold"))

window.mainloop()