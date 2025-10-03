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

def addXMinutes(time):
    current_value = 0
    try:
        current_value = int(timeEntry.get())
    except ValueError:
        current_value = 0
    
    if current_value <= 0:
        if time < 0:
            statusLabel.configure(text="Please do not try to go under 0.")
            return 
        current_value = 0
    
    new_value = current_value + time
    statusLabel.configure(text=f"Added {time} minute(s). Choose an action or add/remove time.")
    
    timeEntry.delete(0, "end")
    timeEntry.insert(0, str(new_value))

def showCustomToast(action, minutes):
    if minutes == 0:
        message = "Your PC will action in 10 seconds."
    else:
        message = f"Your PC will {action} in {minutes} minute(s)."
    notification.notify(
        title=f'Goodnight: {action.capitalize()} scheduled!',
        message=message, app_name='GoodNight', app_icon=None, timeout=5
    )

def scheduleAction(action):
    global isAProcessRunning
    if isAProcessRunning:
        statusLabel.configure(text="An action is already scheduled.\nCancel it before starting a new one.")
        return

    try:
        minutes = int(timeEntry.get())
        if minutes < 0:
            statusLabel.configure(text="Please enter a positive number.")
            return
        elif minutes == 0:
            seconds = 10
        else:
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
                os.makedirs(STATUS_DIR, exist_ok=True)
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
        statusLabel.configure(text="Invalid input. Please enter 0 or more minutes.")

def cancelAction():
    global isAProcessRunning
    if not isAProcessRunning:
        statusLabel.configure(text="There is no action to be cancelled.")
        return

    system = platform.system()
    if system == "Windows":
        CREATE_NO_WINDOW = 0x08000000
        subprocess.run(["shutdown", "/a"], capture_output=True, creationflags=CREATE_NO_WINDOW)
        subprocess.run(["taskkill", "/F", "/IM", "timeout.exe"], capture_output=True, creationflags=CREATE_NO_WINDOW)
        
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
root.geometry('550x400') # Increased height slightly for the new layout
root.resizable(False, False)

# ----- GUI ----- #
frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(pady=20, padx=20,fill="both", expand=True)

inputFrame = ctk.CTkFrame(frame, fg_color="transparent")
inputFrame.pack(pady=10)

label = ctk.CTkLabel(inputFrame, text="Time in minutes:", font=("Segoe UI", 16))
label.pack(side="left", padx=(0, 10))

timeEntry = ctk.CTkEntry(inputFrame, 
                         width=100, 
                         height=40, 
                         font=("Segoe UI", 18), 
                         corner_radius=10)
timeEntry.pack(side="left")
timeEntry.focus()

# ----- ALL BUTTONS MAIN CONTAINER ----- #
buttonsContainer = ctk.CTkFrame(frame, fg_color="transparent")
buttonsContainer.pack(pady=10, fill="x", expand=True)

# ----- TIME SUGGESTION BUTTONS FRAME ----- #
timeButtonsFrame = ctk.CTkFrame(buttonsContainer, fg_color="transparent")
timeButtonsFrame.pack(side="left", padx=10, expand=True)

addTimeButtonsFrame = ctk.CTkFrame(timeButtonsFrame, fg_color="transparent")
addTimeButtonsFrame.pack(side="left", padx=10)

removeTimeButtonsFrame = ctk.CTkFrame(timeButtonsFrame, fg_color="transparent")
removeTimeButtonsFrame.pack(side="right", padx=2)


addOneMinuteButton = ctk.CTkButton(addTimeButtonsFrame,
                                text="+1 min",command=lambda:addXMinutes(1), 
                                 width=90, height=45,
                                 font=('Segoe UI', 14, 'bold'),corner_radius=15, 
                                 fg_color="#333333",  hover_color="#555555")
addOneMinuteButton.pack(pady=10)

rmOneMinuteButton = ctk.CTkButton(removeTimeButtonsFrame,
                                 text="-1 min",command=lambda:addXMinutes(-1), 
                                 width=90,height=45,
                                 font=('Segoe UI', 14, 'bold'),corner_radius=15, 
                                 fg_color="#d11e45", hover_color="#ff0048")
rmOneMinuteButton.pack(pady=10)
addTenMinutesButton = ctk.CTkButton(addTimeButtonsFrame,
                                 text="+10 min",command=lambda:addXMinutes(10), 
                                 width=90,height=45,
                                 font=('Segoe UI', 14, 'bold'),corner_radius=15, 
                                 fg_color="#333333", hover_color="#555555",)
addTenMinutesButton.pack(pady=10)


rmTenMinutesButton = ctk.CTkButton(removeTimeButtonsFrame,
                                 text="-10 min",command=lambda:addXMinutes(-10), 
                                 width=90, height=45,
                                 font=('Segoe UI', 14, 'bold'),corner_radius=15, 
                                 fg_color="#d11e45", hover_color="#ff0048")
rmTenMinutesButton.pack(pady=10)


addThirtyMinutesButton = ctk.CTkButton(addTimeButtonsFrame,
                                text="+30 min",command=lambda:addXMinutes(30), 
                                width=90,height=45,
                                font=('Segoe UI', 14, 'bold'),corner_radius=15,
                                fg_color="#333333",hover_color="#555555",)
addThirtyMinutesButton.pack(pady=10)

rmThirtyMinutesButton = ctk.CTkButton(removeTimeButtonsFrame,
                                 text="-30 min",command=lambda:addXMinutes(-30), 
                                 width=90,height=45,
                                 font=('Segoe UI', 14, 'bold'),corner_radius=15, 
                                 fg_color="#d11e45", hover_color="#ff0048")
rmThirtyMinutesButton.pack(pady=10)

# ----- div for separation ----- #
div = ctk.CTkFrame(buttonsContainer,fg_color="#4F4F4F",width=2,height=180,corner_radius=1)
div.pack(side="left", pady=10)

# ----- MAIN ACTION BUTTONS CONTAINER ----- #
actionButtonsFrame = ctk.CTkFrame(buttonsContainer, fg_color="transparent")
actionButtonsFrame.pack(side="right", padx=10, expand=True)

shutdownButton = ctk.CTkButton(actionButtonsFrame, 
                               text="Shutdown", command=lambda: scheduleAction('shutdown'), 
                               font=('Segoe UI', 14, 'bold'),corner_radius=15, 
                               height=45, width=180, 
                               fg_color="#6600cc", hover_color="#9d00ff")
shutdownButton.pack(pady=10)

sleepButton = ctk.CTkButton(actionButtonsFrame, 
                             text="Sleep / Hibernate", command=lambda: scheduleAction('sleep'), 
                             font=('Segoe UI', 14, 'bold'), corner_radius=15, 
                             height=45, width=180, 
                             fg_color="#2a75bb", hover_color="#3697e1")
sleepButton.pack(pady=10)

cancelButton = ctk.CTkButton(actionButtonsFrame, 
                               text="Cancel Action", command=cancelAction, 
                               font=('Segoe UI', 14, 'bold'), corner_radius=15, 
                               height=45, width=180, 
                               fg_color="#d11e45", hover_color="#ff0048")
cancelButton.pack(pady=10)

# --- Status Label at the bottom ---
statusLabel = ctk.CTkLabel(frame, text="Enter a time and choose an action.", font=("Segoe UI", 14))
statusLabel.pack(pady=(15, 10), side="bottom")

# ----- INITIALIZATION ----- #
checkForExistingAction()
root.mainloop()