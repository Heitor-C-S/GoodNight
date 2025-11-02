import customtkinter as ctk
from plyer import notification

class Utils:
    def __init__(self, controller):
        self.controller = controller
  
    def showCustomToast(self, action, minutes):
        if minutes == 0:
            message = "Your PC will action in 10 seconds."
        else:
            message = f"Your PC will {action} in {minutes} minute(s)."
        notification.notify(
            title=f'Goodnight: {action.capitalize()} scheduled!',
            message=message, app_name='GoodNight', app_icon=None, timeout=5
        )

    # ----- FUNCTION TO CREATE WIDGETS ----- #
    def create_widgets(self):
        
        frame = ctk.CTkFrame(self.controller.root, fg_color="transparent")
        frame.pack(pady=20, padx=20,fill="both", expand=True)

        inputFrame = ctk.CTkFrame(frame, fg_color="transparent")
        inputFrame.pack(pady=10)

        label = ctk.CTkLabel(inputFrame, text="Time in minutes:", font=("Segoe UI", 16))
        label.pack(side="left", padx=(0, 10))

        # ----- STORAGING WIDGETS IN 'SELF' STATE ----- #
        self.controller.timeEntry = ctk.CTkEntry(inputFrame, 
                                      width=100, 
                                      height=40, 
                                      font=("Segoe UI", 18), 
                                      corner_radius=10)
        self.controller.timeEntry.pack(side="left")
        self.controller.timeEntry.focus()

        return frame
