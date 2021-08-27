from tkinter import *
from PIL import ImageTk, Image
import time
import datetime
import threading
from picamera import PiCamera
from sense_hat import SenseHat
import serial
from slickk_api import classify_syringe

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
            self.medium = ("Helvetica", 20)
            self.small = ("Helvetica", 14)
            Font.__instance = self


# HELPER METHODS FOR DISPLAYING & HIDING WIDGETS

def displayWelcomeWidgets():
    # Display Welcome Screen Widgets
    welcome_lbl.place(relx=0.5, rely=0.05, anchor=N)
    button_settings.place(relx=0.95, rely=0.1, anchor=E)
    syringe_lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
    button_start.place(relx=0.5, rely=0.95, anchor=S)

def hideWelcomeWidgets():
    # Hide all Widgets for Welcome Screen
    welcome_lbl.place_forget()
    button_settings.place_forget()
    syringe_lbl.place_forget()
    button_start.place_forget()

def displaySettingsWidgets():
    settings_txt_lbl.place(relx=0.5, rely=0.05, anchor=N)
    button_back_settings.place(relx=0.1, rely=0.1, anchor=W)
    button_wash_tank.place(relx=0.1, rely=0.3)
    last_washed_lbl.place(relx=0.1, rely=0.42)

def hideSettingsWidgets():
    settings_txt_lbl.place_forget()
    button_back_settings.place_forget()
    button_wash_tank.place_forget()
    last_washed_lbl.place_forget()

def displayWashTankWidgets():
    washing_tank_txt_lbl.pack(pady=10)
    placeholder_img_lbl.pack(pady=5)
    countdown_lbl.pack(pady=10)

def hideWashTankWidgets():
    washing_tank_txt_lbl.pack_forget()
    placeholder_img_lbl.pack_forget()
    countdown_lbl.pack_forget()

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
    placeholder_img_lbl.pack(pady=5)
    countdown_lbl.pack(pady=10)

def hideWashingWidgets():
    washing_txt_lbl.pack_forget()
    placeholder_img_lbl.pack_forget()
    countdown_lbl.pack_forget()

def displayDryingWidgets():
    drying_txt_lbl.pack(pady=10)
    placeholder_img_lbl.pack(pady=5)
    countdown_lbl.pack(pady=10)

def hideDryingWidgets():
    drying_txt_lbl.pack_forget()
    placeholder_img_lbl.pack_forget()
    countdown_lbl.pack_forget()

def displaySterilizingWidgets():
    sterilizing_txt_lbl.pack(pady=10)
    placeholder_img_lbl.pack(pady=5)
    countdown_lbl.pack(pady=10)

def hideSterilizingWidgets():
    sterilizing_txt_lbl.pack_forget()
    placeholder_img_lbl.pack_forget()
    countdown_lbl.pack_forget()

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

def settings():
    hideWelcomeWidgets()
    displaySettingsWidgets()

def wash_tank():
    hideSettingsWidgets()
    displayWashTankWidgets()

    threading.Thread(target=wash_tank2).start()

def back():
    hideInsertSyringesWidgets()
    displayWelcomeWidgets()

def back_from_settings():
    hideSettingsWidgets()
    displayWelcomeWidgets()

def okay():
    hideReadyWidgets()
    displayWelcomeWidgets()

def start_washing():
    hideInsertSyringesWidgets()
    displayWashingWidgets()

    threading.Thread(target=wash).start()


# METHODS FOR WASHING, DRYING, STERILIZING

def switchOnLights():
    white = [255,255,255]
    pixels = [
        white, white, white, white, white, white, white, white,
        white, white, white, white, white, white, white, white,
        white, white, white, white, white, white, white, white,
        white, white, white, white, white, white, white, white,
        white, white, white, white, white, white, white, white,
        white, white, white, white, white, white, white, white,
        white, white, white, white, white, white, white, white,
        white, white, white, white, white, white, white, white
        ]
    sense.set_pixels(pixels)

def switchOffLights():
    sense.clear()
    
def check_lid_status():
    while True:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        if line == "lid_open":
            # Disable start washing button
            button_start_washing.config(state="disabled")
        elif line == "lid_closed":
            # Enable start washing button
            button_start_washing.config(state="normal")
            break

def wash():

    camera.start_preview(fullscreen=False,window=(210,115,400,300))
    
    ser.write(b"fill\n") # activate arduino water pump

    countdown(70)
    
    countdown_lbl.config(text = "Checking if\nsyringes are clean. Please wait...")
    file_path = 'syringe.jpg'
    switchOnLights()
    camera.capture(file_path)
    switchOffLights()
    classification = classify_syringe(file_path)
    
#     msg = "Syringes are clean.\nNow drying the syringes..."
#     print(msg)
#     countdown_lbl.config(text = msg)
#     time.sleep(2)
#     hideWashingWidgets()
#     displayDryingWidgets()
# 
#     threading.Thread(target=dry).start()
    
    if classification == 'clean':
        msg = "Syringes are clean.\nNow drying the syringes..."
        print(msg)
        countdown_lbl.config(text = msg)
        time.sleep(2)
        hideWashingWidgets()
        displayDryingWidgets()

        threading.Thread(target=dry).start()
    else:
        msg = "Syringes are still dirty. Restarting washing cycle..."
        print(msg)
        countdown_lbl.config(text = msg)
        time.sleep(2)
        wash()


def wash_tank2():
    # TODO: activate the water pump
    camera.start_preview(fullscreen=False,window=(210,115,400,300))
    countdown(70)
    camera.stop_preview()
    hideWashTankWidgets()
    displayWelcomeWidgets()

    # Set last washed date to now
    with open('last_washed_date.txt', 'w') as f:
        now = datetime.datetime.now()
        now_text = now.strftime('%c')
        f.write(now_text)

        temp = "Last washed: " + now_text
        last_washed_lbl.config(text = temp)


def dry():
    ser.write(b"dry\n") # activate arduino fans
    countdown(40)
    
    countdown_lbl.config(text = "Checking if\nsyringes are dry. Please wait...")
    ser.write(b"humidity\n")
    while True:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        if line == 'dry':
            msg = "Syringes are dry.\nNow sterilizing the syringes..."
            print(msg)
            countdown_lbl.config(text = msg)
            time.sleep(2)

            hideDryingWidgets()
            displaySterilizingWidgets()

            threading.Thread(target=sterilize).start()
            break
        elif line == 'wet':
            msg = "Syringes are still wet. Restarting drying cycle..."
            print(msg)
            countdown_lbl.config(text = msg)
            time.sleep(2)
            dry()
            break


def sterilize():
    ser.write(b"sterilize\n") # activate arduino uv light
    countdown(30)
    camera.stop_preview()

    hideSterilizingWidgets()
    displayReadyWidgets()
    ser.write(b"done\n")

def countdown(duration):
    for x in range(duration):
        time_left = duration-x
        time_left_txt = "Remaining time: " + str(time_left) + "s"
        countdown_lbl.config(text = time_left_txt)
        time.sleep(1)  # one second


# Configure application
root = Tk()
root.geometry('800x480')
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.title("SteriDry")
    
# Define images
placeholder_img = ImageTk.PhotoImage(Image.open("images/placeholder.jpg"))
syringe_img = ImageTk.PhotoImage(Image.open("images/logo.png"))
insert_syringe_img = ImageTk.PhotoImage(Image.open("images/insert_syringes.jpg"))
washing_img = ImageTk.PhotoImage(Image.open("images/washing.jpg"))
drying_img = ImageTk.PhotoImage(Image.open("images/drying.jpg"))
sterilizing_img = ImageTk.PhotoImage(Image.open("images/sterilizing.jpg"))
success_img = ImageTk.PhotoImage(Image.open("images/success.png"))
settings_img = ImageTk.PhotoImage(Image.open("images/settings.png"))

placeholder_img_lbl = Label(image=placeholder_img)

# Define Tkinter Widgets for Welcome Screen
global welcome_lbl
global button_settings
global syringe_lbl
global button_start
welcome_lbl = Label(text="Welcome to SteriDry!", font=(Font.getInstance().large))
button_settings = Button(root, image=settings_img, font=(Font.getInstance().medium), command=settings)
syringe_lbl = Label(image=syringe_img)
button_start = Button(root, text="START", font=(Font.getInstance().medium), command=start)

# Define Tkinter Widgets for Settings Screen
global settings_txt_lbl
global button_wash_tank
global last_washed_lbl
global button_back_settings
settings_txt_lbl = Label(text="Settings", font=(Font.getInstance().large))
button_wash_tank = Button(root, text="Wash Tank", font=(Font.getInstance().medium), command=wash_tank)
last_washed_date = ""
with open('last_washed_date.txt') as f:
    last_washed_date = f.read()
last_washed_date_txt = "Last washed: " + last_washed_date
last_washed_lbl = Label(text=last_washed_date_txt, font=(Font.getInstance().small))
button_back_settings = Button(root, text="<", font=(Font.getInstance().small), command=back_from_settings)

# Define Widgets for "Washing Tank" screen
global washing_tank_txt_lbl
washing_tank_txt_lbl = Label(text="Washing Tank...", font=(Font.getInstance().large))

# Define Widgets for "Insert Syringes" screen
global please_insert_lbl
global insert_syringe_lbl
global button_back
global button_start_washing
please_insert_lbl = Label(text="Please Insert Your Syringes for Washing...", font=(Font.getInstance().large))
insert_syringe_lbl = Label(image=insert_syringe_img)
button_back = Button(root, text="BACK", font=(Font.getInstance().medium), command=back)
button_start_washing = Button(root, text="START WASHING", font=(Font.getInstance().medium), command=start_washing)

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
button_okay = Button(root, text="OKAY", font=(Font.getInstance().medium), command=okay)

# Define Widgets for Countdown timer
countdown_lbl = Label(text="", font=(Font.getInstance().medium))  # in main thread

# Define camera & sensehat
camera = PiCamera()
sense = SenseHat()

# Configure rpi to arduino communication
global ser
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
ser.flush()

threading.Thread(target=check_lid_status).start()
        
# Upon running this Python script, display Widgets for Welcome Screen
displayWelcomeWidgets()
root.mainloop()
