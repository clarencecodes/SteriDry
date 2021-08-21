from tkinter import *
from PIL import ImageTk, Image
import time
import threading

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
            self.large = ("Helvetica", 28)
            self.small = ("Helvetica", 20)
            Font.__instance = self


# HELPER METHODS FOR DISPLAYING & HIDING WIDGETS

def displayWelcomeWidgets():
    # Display Welcome Screen Widgets
    welcome_lbl.pack(pady=10)
    syringe_lbl.pack(pady=5)
    button_start.pack(pady=10)
    
def hideWelcomeWidgets():
    # Hide all Widgets for Welcome Screen
    welcome_lbl.pack_forget()
    syringe_lbl.pack_forget()
    button_start.pack_forget()
    
def displayInsertSyringesWidgets():
    # Display new Widgets
    please_insert_lbl.grid(row=0, column=0, columnspan=2)
    insert_syringe_lbl.grid(row=1, column=0, pady=5, columnspan=2)
    button_back.grid(row=2, column=0, pady=10, columnspan=1)
    button_start_washing.grid(row=2, column=1, pady=10, columnspan=1)
    
def hideInsertSyringesWidgets():
    # Hide all Widgets for "Insert Syringes" screen
    please_insert_lbl.grid_forget()
    insert_syringe_lbl.grid_forget()
    button_back.grid_forget()
    button_start_washing.grid_forget()
    
def displayWashingWidgets():
    washing_txt_lbl.pack(pady=10)
    washing_img_lbl.pack(pady=5)
    
def hideWashingWidgets():
    washing_txt_lbl.pack_forget()
    washing_img_lbl.pack_forget()
    
def displayDryingWidgets():
    drying_txt_lbl.pack(pady=10)
    drying_img_lbl.pack(pady=5)

def hideDryingWidgets():
    drying_txt_lbl.pack_forget()
    drying_img_lbl.pack_forget()
    
def displaySterilizingWidgets():
    sterilizing_txt_lbl.pack(pady=10)
    sterilizing_img_lbl.pack(pady=5)
    
def hideSterilizingWidgets():
    sterilizing_txt_lbl.pack_forget()
    sterilizing_img_lbl.pack_forget()
    
def displayReadyWidgets():
    ready_txt_lbl.pack(pady=10)
    ready_img_lbl.pack(pady=5)
    button_okay.pack(pady=10)

def hideReadyWidgets():
    ready_txt_lbl.pack_forget()
    ready_img_lbl.pack_forget()
    button_okay.pack_forget()

# METHODS FOR USER INTERACTION

def start():
    hideWelcomeWidgets()
    displayInsertSyringesWidgets()
    
def back():
    hideInsertSyringesWidgets()
    displayWelcomeWidgets()
    
def okay():
    hideReadyWidgets()
    displayWelcomeWidgets()

def start_washing():
    hideInsertSyringesWidgets()
    displayWashingWidgets()
    
    threading.Thread(target=wash).start()


# METHODS FOR WASHING, DRYING, STERILIZING

def wash():
    # TODO: activate the camera/ML function and water pump instead
    time.sleep(3)
    
    hideWashingWidgets()
    displayDryingWidgets()
    
    threading.Thread(target=dry).start() 
    
def dry():
    # TODO: display the camera, and activate the humidity sensor
    time.sleep(3)
    
    hideDryingWidgets()
    displaySterilizingWidgets()
    
    threading.Thread(target=sterilize).start()
    
def sterilize():
    # TODO: display the camera/ML function, and activate the UV light
    time.sleep(3)
    
    hideSterilizingWidgets()
    displayReadyWidgets()

# Configure application
root = Tk()
root.geometry('800x480')
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.title("SteriDry")

# Define images
global syringe_img
global insert_syringe
global washing_img
global drying_img
global sterilizing_img
global success_img
syringe_img = ImageTk.PhotoImage(Image.open("images/syringe.png"))
insert_syringe_img = ImageTk.PhotoImage(Image.open("images/insert_syringes.jpg"))
washing_img = ImageTk.PhotoImage(Image.open("images/washing.jpg"))
drying_img = ImageTk.PhotoImage(Image.open("images/drying.jpg"))
sterilizing_img = ImageTk.PhotoImage(Image.open("images/sterilizing.jpg"))
success_img = ImageTk.PhotoImage(Image.open("images/success.png"))

# Define Tkinter Widgets for Welcome Screen
global welcome_lbl
global syringe_lbl
global button_start
welcome_lbl = Label(text="Welcome to SteriDry!", font=(Font.getInstance().large))
syringe_lbl = Label(image=syringe_img)
button_start = Button(root, text="START", font=(Font.getInstance().small), command=start)

# Define Widgets for "Insert Syringes" screen
global please_insert_lbl
global insert_syringe_lbl
global button_back
global button_start_washing
please_insert_lbl = Label(text="Please Insert Your Syringes for Washing...", font=(Font.getInstance().large))
insert_syringe_lbl = Label(image=insert_syringe_img)
button_back = Button(root, text="BACK", font=(Font.getInstance().small), command=back)
button_start_washing = Button(root, text="START WASHING", font=(Font.getInstance().small), command=start_washing)

# Define Widgets for "Washing" Screen
global washing_txt_lbl
global washing_img_lbl
washing_txt_lbl = Label(text="Washing...", font=(Font.getInstance().large))
washing_img_lbl = Label(image=washing_img)

# Define Widgets for "Drying" Screen
global drying_txt_lbl
global drying_img_lbl
drying_txt_lbl = Label(text="Drying...", font=(Font.getInstance().large))
drying_img_lbl = Label(image=drying_img)

# Define Widgets for "Sterilizing" Screen
global sterilizing_txt_lbl
global sterilizing_img_lbl
sterilizing_txt_lbl = Label(text="Sterilizing...", font=(Font.getInstance().large))
sterilizing_img_lbl = Label(image=sterilizing_img)

# Define Widgets for "Syringes Ready" Screen
global ready_txt_lbl
global ready_img_lbl
global button_okay
ready_txt_lbl = Label(text="Syringes are cleaned\nand ready for use.", font=(Font.getInstance().large))
ready_img_lbl = Label(image=success_img)
button_okay = Button(root, text="OKAY", font=(Font.getInstance().small), command=okay)

# Upon running this Python scrupt, display Widgets for Welcome Screen
displayWelcomeWidgets()
root.mainloop()