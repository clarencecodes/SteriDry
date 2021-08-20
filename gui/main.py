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
            self.large = ("Helvetica", 30)
            self.small = ("Helvetica", 16)
            Font.__instance = self

def start():
    # Hide all Widgets for Welcome Screen
    welcome_lbl.pack_forget()
    syringe_lbl.pack_forget()
    button_start.pack_forget()
    
    # Define Widgets for "Insert Syringes" screen
    please_insert_lbl = Label(text="Please Insert Your Syringes for Washing...", font=(Font.getInstance().large))
    insert_syringe_lbl = Label(image=insert_syringe_img)
    button_back = Button(root, text="Back", font=(Font.getInstance().small), command=back)
    button_start_washing = Button(root, text="Start Washing", font=(Font.getInstance().small), command=start_washing)
    
    # Display new Widgets
    please_insert_lbl.grid(row=0, column=0, padx= 20, pady=20, columnspan=2)
    insert_syringe_lbl.grid(row=1, column=0, pady=10, columnspan=2)
    button_back.grid(row=2, column=0, pady=20, columnspan=1)
    button_start_washing.grid(row=2, column=1, pady=20, columnspan=1)
    
def back():
    return

def start_washing():
    return
    
    
root = Tk()
root.geometry('800x480')
root.title("SteriDry")

# Define images
global syringe_img
global insert_syringe
global washing_img
global drying_img
global sterilizing_img
syringe_img = ImageTk.PhotoImage(Image.open("images/syringe.png"))
insert_syringe_img = ImageTk.PhotoImage(Image.open("images/insert_syringes.jpg"))
washing_img = ImageTk.PhotoImage(Image.open("images/washing.jpg"))
drying_img = ImageTk.PhotoImage(Image.open("images/drying.jpg"))
sterilizing_img = ImageTk.PhotoImage(Image.open("images/sterilizing.jpg"))

# Define Tkinter Widgets for Welcome Screen
welcome_lbl = Label(text="Welcome to SteriDry!", font=(Font.getInstance().large))
syringe_lbl = Label(image=syringe_img)
button_start = Button(root, text="Start", font=(Font.getInstance().small), command=start)

# Display Widgets
welcome_lbl.pack(pady=20)
syringe_lbl.pack(pady=10)
button_start.pack(pady=20)