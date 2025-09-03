import customtkinter as ctk
import os
import platform
import subprocess
from plyer import notification
import json
import time
from appdirs import user_data_dir

# ----- PERSISTENCE CONFIG ----- #
APP_NAME = "GoodNight"
APP_AUTHOR = "HCS"
STATUS_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
STATUS_FILE = os.path.join(STATUS_DIR, "status.json")

isAProcessRunning = False

# ----- FUNCTIONS DEFINITION -----#

def showCustomToast(action, minutes):
    message = f"Your PC will {action} in {minutes} minute(s)."
    if minutes < 1:
        message = f"Your PC will {action} in {int(minutes * 60)} second(s)."
    notification.notify(
        title=f'Goodnight: {action.capitalize()} scheduled!',
        message=message, app_name='GoodNight', app_icon=None, timeout=10
    )

def scheduleAction(action):
    global isAProcessRunning
    if isAProcessRunning:
        statusLabel.configure(text="An action is already scheduled.\nCancel it before starting a new one.")
        return

    try:
        minutes = int(timeEntry.get())
        if minutes <= 0:
            statusLabel.configure(text="Please enter a positive number.")
            return

        seconds = minutes * 60
        system = platform.system()
        command = ""

        if system == "Windows":
            if action == 'shutdown':
                command = f"shutdown /s /t {seconds}"
            elif action == 'sleep':
                command = f"timeout /t {seconds} /nobreak && shutdown /h"
                action = 'hibernate'

        if command:
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(command, shell=True, creationflags=CREATE_NO_WINDOW)
            
            try:
                end_time = time.time() + seconds
                status_data = {"action": action, "end_time": end_time}
                os.makedirs(STATUS_DIR, exist_ok=True) # Create the safe directory
                with open(STATUS_FILE, "w") as f:
                    json.dump(status_data, f)
            except OSError as e:
                print(f"FAILED TO WRITE STATUS FILE: {e} ")

            isAProcessRunning = True
            showCustomToast(action, minutes)
            statusLabel.configure(text=f"PC will {action} in {minutes} minute(s).")
        else:
            statusLabel.configure(text=f"Action not supported on {system}.")
    except ValueError:
        statusLabel.configure(text="Invalid input. Please enter minutes.")


def cancelAction():
    global isAProcessRunning

    if isAProcessRunning == True:
        system = platform.system()
        if system == "Windows":
            CREATE_NO_WINDOW = 0x08000000
            subprocess.run(["shutdown", "/a"], capture_output=True, creationflags=CREATE_NO_WINDOW)
            
            if os.path.exists(STATUS_FILE):
                try:
                    os.remove(STATUS_FILE)
                except OSError as e:
                    print(f"Error removing status file: {e}")

            isAProcessRunning = False
            statusLabel.configure(text="Scheduled action canceled.")
            notification.notify(
                title="Goodnight: Canceled!", message="The scheduled action was successfully canceled.",
                app_name='GoodNight', app_icon=None, timeout=5
            )
    else:
        statusLabel.configure(text="There is nothing to be cancelled right now.")

def checkForExistingAction():
    """This function runs once at startup to check the flag file."""
    global isAProcessRunning
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, "r") as f:
                status_data = json.load(f)
            
            if time.time() < status_data.get("end_time", 0):
                isAProcessRunning = True
                action = status_data.get("action", "unknown action")
                statusLabel.configure(text=f"An active '{action}' is already scheduled.")
            else:
                os.remove(STATUS_FILE)
                isAProcessRunning = False
        except (json.JSONDecodeError, FileNotFoundError, OSError):
            isAProcessRunning = False


# ----- APP SETUP & WINDOW ----- #
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("GoodNight")
root.geometry('550x350')
root.resizable(False, False)

# ----- GUI ----- #
frame = ctk.CTkFrame(root, 
                     fg_color="transparent")
frame.pack(pady=20, 
           padx=20, 
           fill="both", 
           expand=True)

inputFrame = ctk.CTkFrame(frame, 
                          fg_color="transparent")
inputFrame.pack(pady=10)

label = ctk.CTkLabel(inputFrame, 
                     text="Time in minutes:", 
                     font=("Segoe UI", 16))
label.pack(side="left", padx=(0, 10))

timeEntry = ctk.CTkEntry(inputFrame, width=150, height=40, font=("Segoe UI", 18), corner_radius=10)
timeEntry.pack(side="left")
timeEntry.focus()

shutdownButton = ctk.CTkButton(frame, text="Shutdown", command=lambda: scheduleAction('shutdown'), font=('Segoe UI', 14, 'bold'), corner_radius=15, height=45, width=300, fg_color="#6600cc", hover_color="#9d00ff")
shutdownButton.pack(pady=10)

sleepButton = ctk.CTkButton(frame, text="Sleep / Hibernate", command=lambda: scheduleAction('sleep'), font=('Segoe UI', 14, 'bold'), corner_radius=15, height=45, width=300, fg_color="#2a75bb", hover_color="#3697e1")
sleepButton.pack(pady=10)

cancelButton = ctk.CTkButton(frame, 
                             text="Cancel Action", 
                             command=cancelAction, 
                             font=('Segoe UI', 14, 'bold'), 
                             corner_radius=15, 
                             height=45, 
                             width=300, 
                             fg_color="#d11e45", 
                             hover_color="#ff0048")
cancelButton.pack(pady=10)

statusLabel = ctk.CTkLabel(frame, 
                           text="Enter a time and choose an action.", 
                           font=("Segoe UI", 14))
statusLabel.pack(pady=(15, 10))


# ----- INITIALIZATION ----- #
checkForExistingAction()

root.mainloop()