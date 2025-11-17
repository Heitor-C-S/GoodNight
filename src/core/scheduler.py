# ----- core/scheduler.py ----- #
import json
import os
import platform
import subprocess
import time
from plyer import notification
from appdirs import user_data_dir

# ----- PERSISTENCY CONSTANTS ----- #
APP_NAME = "GoodNight"
APP_AUTHOR = "HCS"
STATUS_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
STATUS_FILE = os.path.join(STATUS_DIR, "status.json")


class Scheduler:
    def __init__(self, controller):
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

    def _checkHibernationEnabled(self):
        """Check if hibernation is enabled on the system."""
        try:
            result = subprocess.run(
                ["powercfg", "/a"],
                capture_output=True,
                text=True,
                creationflags=0x08000000
            )
            return "hibernate" in result.stdout.lower() and "not supported" not in result.stdout.lower()
        except:
            return False

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
            if system != "Windows":
                self.controller.statusLabel.configure(text=f"Action not supported on {system}.")
                return

            CREATE_NO_WINDOW = 0x08000000
            
            if action == 'shutdown':
                command = ["shutdown", "/s", "/t", str(seconds)]
                subprocess.Popen(command, creationflags=CREATE_NO_WINDOW)
                
                end_time = time.time() + seconds
                self._saveStatus(action, end_time)
                
            elif action in ['sleep', 'hibernate']:
                # Check if hibernation is enabled
                if not self._checkHibernationEnabled():
                    self.controller.statusLabel.configure(
                        text="Hibernation is disabled on your system.\nRun 'powercfg /h on' in Admin CMD to enable."
                    )
                    return

                # Use rundll32 for explicit hibernation (more reliable than shutdown /h)
                ps_script = f'''
$seconds = {seconds}
$statusFile = "{STATUS_FILE}"
Start-Sleep -Seconds $seconds
if (Test-Path $statusFile) {{ Remove-Item $statusFile -Force }}
# Hibernation command - only works if hibernation is enabled
rundll32.exe powrprof.dll,SetSuspendState 1,1,0
'''
                command = [
                    "powershell.exe",
                    "-WindowStyle", "Hidden",
                    "-NoLogo",
                    "-NonInteractive",
                    "-Command", ps_script
                ]
                self.controller.hibernate_process = subprocess.Popen(
                    command, creationflags=CREATE_NO_WINDOW
                )
            
            self.controller.isAProcessRunning = True 
            self.controller.showCustomToast(action, minutes) 
            self.controller.statusLabel.configure(text=f"PC will {action} in {minutes} minute(s).")
            
        except ValueError:
            self.controller.statusLabel.configure(text="Invalid input. Please enter 0 or more minutes.")

    def _saveStatus(self, action, end_time):
        """Helper to save status file for shutdown actions."""
        try:
            os.makedirs(STATUS_DIR, exist_ok=True)
            with open(STATUS_FILE, "w") as f:
                json.dump({"action": action, "end_time": end_time}, f)
        except OSError as e:
            print(f"FAILED TO WRITE STATUS FILE: {e}")

    def cancelAction(self):
        if not self.controller.isAProcessRunning:
            self.controller.statusLabel.configure(text="There is no action to be cancelled.")
            return

        system = platform.system()
        if system == "Windows":
            CREATE_NO_WINDOW = 0x08000000
            
            # Kill PowerShell hibernation process if it exists
            if self.controller.hibernate_process:
                try:
                    self.controller.hibernate_process.kill()
                except ProcessLookupError:
                    pass
                self.controller.hibernate_process = None

            # Cancel native Windows shutdown
            subprocess.run(["shutdown", "/a"], capture_output=True, creationflags=CREATE_NO_WINDOW)
            
            # Clean up status file
            if os.path.exists(STATUS_FILE):
                try:
                    os.remove(STATUS_FILE)
                except OSError as e:
                    print(f"Error removing status file: {e}")

            self.controller.isAProcessRunning = False
            self.controller.statusLabel.configure(text="Scheduled action canceled.")
            notification.notify(
                title="Goodnight: Canceled!", message="The scheduled action was successfully canceled.",
                app_name='GoodNight', timeout=5
            )

    def checkForExistingAction(self):
        """Checks for existing shutdown action on app start."""
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, "r") as f:
                    status_data = json.load(f)
                
                if time.time() < status_data.get("end_time", 0):
                    self.controller.isAProcessRunning = True
                    action = status_data.get("action", "unknown action")
                    self.controller.statusLabel.configure(text=f"An active '{action}' is already scheduled.")
                else:
                    os.remove(STATUS_FILE)
                    self.controller.isAProcessRunning = False
            except (json.JSONDecodeError, FileNotFoundError, OSError):
                if os.path.exists(STATUS_FILE):
                    try: os.remove(STATUS_FILE)
                    except OSError: pass
                self.controller.isAProcessRunning = False
        else:
            self.controller.isAProcessRunning = False
