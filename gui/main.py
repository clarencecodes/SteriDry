from tkinter import *
from PIL import ImageTk, Image

class Font:
    __instance = None
    
    @staticmethod
    def getInstance():
        if Font.__instance == None:
            Font()
        return Font.__instance
    
    def __init__(self):
        if Font.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.large = ("Helvetica", 32)
            self.small = ("Helvetica", 16)
            Font.__instance = self

def start():
    button_start.pack()
    return

root = Tk()
root.geometry('800x480')
root.title("SteriDry")

welcome_lbl = Label(text="Welcome to SteriDry!", font=(Font.getInstance().large))
syringe_img = ImageTk.PhotoImage(Image.open("images/syringe.png"))
syringe_lbl = Label(image=syringe_img)
button_start = Button(root, text="Start", font=(Font.getInstance().small), command=start)

welcome_lbl.pack(pady=20)
syringe_lbl.pack(pady=10)
button_start.pack(pady=20)