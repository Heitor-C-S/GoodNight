import customtkinter as ctk

from gui import buttons
from core.scheduler import Scheduler
from core.utils import Utils

# ----- CLASS GOODNIGHT ----- #
class GoodNightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GoodNight")
        self.root.geometry('550x400')
        self.root.resizable(False, False)
        self.utils = Utils(self)
        self.scheduler = Scheduler(self)
        self.isAProcessRunning = False
        self.create_widgets()
        self.scheduler.checkForExistingAction()
           
   
    def addXMinutes(self,time_to_add):
        self.scheduler.addXMinutes(time_to_add)
    
    def scheduleAction(self,action):
        self.scheduler.scheduleAction(action)

    def cancelAction(self):
        self.scheduler.cancelAction()

    def showCustomToast(self, action, minutes):
        self.utils.showCustomToast(action,minutes)

    # ----- FUNCTION TO CREATE WIDGETS ----- #
    def create_widgets(self):
        frame = self.utils.create_widgets()

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

        # ----- DIV FOR SEPARATION ----- #
        div = ctk.CTkFrame(buttonsContainer,fg_color="#4F4F4F",width=2,height=180,corner_radius=1)
        div.pack(side="left", pady=10)

        # ----- MAIN ACTION BUTTONS CONTAINER ----- #
        actionButtonsFrame = ctk.CTkFrame(buttonsContainer, fg_color="transparent")
        actionButtonsFrame.pack(side="right", padx=10, expand=True)

        # ----- INSTANCING STATUS LABEL ----- #
        self.statusLabel = ctk.CTkLabel(frame, text="Enter a time and choose an action.", font=("Segoe UI", 14))
        self.statusLabel.pack(pady=(15, 10), side="bottom")

        # ----- INSTANCING TIME BUTTONS ----- #
        buttons.create_time_buttons(addTimeButtonsFrame, removeTimeButtonsFrame, self)
        buttons.create_action_buttons(actionButtonsFrame, self)


# ----- APP ENTRY POINT ----- #
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = GoodNightApp(root) 
    root.mainloop()

