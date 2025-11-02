import customtkinter as ctk
import os
import platform
import subprocess
from plyer import notification
import json
import time
from appdirs import user_data_dir

# ----- PERSISTENCY CONSTANTS ----- #
APP_NAME = "GoodNight"
APP_AUTHOR = "HCS"
STATUS_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
STATUS_FILE = os.path.join(STATUS_DIR, "status.json")


class Scheduler:
    def __init__(self, controller):
        """
        Inicia o agendador.
        'controller' é a instância da classe GoodNightApp.
        """
        self.controller = controller

    def addXMinutes(self, time_to_add):
        current_value = 0
        try:
            current_value = int(self.controller.timeEntry.get())
        except ValueError:
            current_value = 0
        
        if current_value <= 0:
            if time_to_add < 0:
                self.controller.statusLabel.configure(text="Please do not try to go under 0.")
                return 
            current_value = 0
        
        new_value = current_value + time_to_add
        self.controller.statusLabel.configure(text=f"Added {time_to_add} minute(s). Choose an action or add/remove time.")
        
        self.controller.timeEntry.delete(0, "end")
        self.controller.timeEntry.insert(0, str(new_value))

    def scheduleAction(self, action):
        if self.controller.isAProcessRunning:
            self.controller.statusLabel.configure(text="An action is already scheduled.\nCancel it before starting a new one.")
            return

        try:
            minutes = int(self.controller.timeEntry.get())
            if minutes < 0:
                self.controller.statusLabel.configure(text="Please enter a positive number.")
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

                self.controller.isAProcessRunning = True 
                self.controller.showCustomToast(action, minutes) 
                self.controller.statusLabel.configure(text=f"PC will {action} in {minutes} minute(s).")
            else:
                self.controller.statusLabel.configure(text=f"Action not supported on {system}.")
        except ValueError:
            self.controller.statusLabel.configure(text="Invalid input. Please enter 0 or more minutes.")

    def cancelAction(self):
        if not self.controller.isAProcessRunning:
            self.controller.statusLabel.configure(text="There is no action to be cancelled.")
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

            self.controller.isAProcessRunning = False
            self.controller.statusLabel.configure(text="Scheduled action canceled.")
            notification.notify(
                title="Goodnight: Canceled!", message="The scheduled action was successfully canceled.",
                app_name='GoodNight', app_icon=None, timeout=5
            )

    def checkForExistingAction(self):
        """Esta função roda na inicialização para checar o arquivo de flag."""
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, "r") as f:
                    status_data = json.load(f)
                
                if time.time() < status_data.get("end_time", 0):
                    self.controller.isAProcessRunning = True
                    action = status_data.get("action", "unknown action")
                    self.controller.statusLabel.configure(text=f"An active '{action}' is already scheduled.")
                else:
                    if os.path.exists(STATUS_FILE):
                        os.remove(STATUS_FILE)
                    self.controller.isAProcessRunning = False
            except (json.JSONDecodeError, FileNotFoundError, OSError):
                if os.path.exists(STATUS_FILE):
                    try: os.remove(STATUS_FILE)
                    except OSError: pass
                self.controller.isAProcessRunning = False
