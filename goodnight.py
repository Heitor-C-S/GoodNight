import tkinter as tk
import customtkinter as ctk
import os
import platform
import subprocess 

# ----- FUNCTIONS DEFINITION -----#
def scheduleAction(action):
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
                # Corrected command for scheduled hibernation
                command = f"timeout /t {seconds} /nobreak && shutdown /h"
                action = 'hibernate'

        if command:
            # Use subprocess.Popen for non-blocking commands
            subprocess.Popen(command, shell=True)
            statusLabel.configure(text=f"PC will {action} in {minutes} minute(s).")
        else:
            statusLabel.configure(text=f"{action.capitalize()} not supported on {system}.")

    except ValueError:
        statusLabel.configure(text="Invalid input. Please enter minutes.")

def cancelAction():
    system = platform.system()
    if system == "Windows":
        # Use subprocess.run to safely execute and hide output
        subprocess.run(["shutdown", "/a"], capture_output=True)
        statusLabel.configure(text="Scheduled action canceled.")

# ----- APP SETUP ----- #
ctk.set_appearance_mode("dark")

# ----- WINDOW PROPERTIES ----- #
root = ctk.CTk()
root.title("GoodNight")
root.geometry('500x300')
root.resizable(False, False)

# ----- GUI ----- #
# The main frame still fills the window
frame = ctk.CTkFrame(root, fg_color="transparent")
frame.pack(pady=20, padx=20, fill="both", expand=True)


# --- Create a sub-frame for the label and entry ---
inputFrame = ctk.CTkFrame(frame, fg_color="transparent")
inputFrame.pack(pady=15) # Pack this frame to center it

label = ctk.CTkLabel(inputFrame, text="Time in minutes:", font=("Segoe UI", 16))
label.pack(side="left", padx=(0, 10)) # Pack label to the left

timeEntry = ctk.CTkEntry(inputFrame, width=150, height=40, font=("Segoe UI", 18), corner_radius=10)
timeEntry.pack(side="left") # Pack entry next to it
timeEntry.focus()

shutdownButton = ctk.CTkButton(
    frame,
    text="Shutdown",
    command=lambda: scheduleAction('shutdown'),
    font=('Segoe UI', 14, 'bold'),
    corner_radius=15,
    height=45,
    width=300,
    fg_color="#6600cc",
    hover_color="#9d00ff"
)
shutdownButton.pack(pady=15, )

cancelButton = ctk.CTkButton(
    frame,
    text="Cancel Action",
    command=cancelAction,
    font=('Segoe UI', 14, 'bold'),
    corner_radius=15,
    height=45,
    width=300,
    fg_color="#d11e45",
    hover_color="#ff0048"
)
cancelButton.pack(pady=10,)

statusLabel = ctk.CTkLabel(frame, text="Enter a time and choose an action.", font=("Segoe UI", 14))
statusLabel.pack(pady=(20, 10))

root.mainloop()