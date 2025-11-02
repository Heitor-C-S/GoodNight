import customtkinter as ctk

def create_time_buttons(add_frame, remove_frame, controller):
    
    # ----- ONE MINUTE BUTTONS ----- #
    addOneMinuteButton = ctk.CTkButton(add_frame,
                                       text="+1 min",
                                       command=lambda: controller.addXMinutes(1), # <-- Chama o método do controller
                                       width=90, height=45,
                                       font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                       fg_color="#333333", hover_color="#555555")
    addOneMinuteButton.pack(pady=10)

    rmOneMinuteButton = ctk.CTkButton(remove_frame,
                                      text="-1 min",
                                      command=lambda: controller.addXMinutes(-1), # <-- Chama o método do controller
                                      width=90, height=45,
                                      font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                      fg_color="#d11e45", hover_color="#ff0048")
    rmOneMinuteButton.pack(pady=10)

    # ----- TEN MINUTES BUTTONS ----- #
    addTenMinutesButton = ctk.CTkButton(add_frame,
                                        text="+10 min",
                                        command=lambda: controller.addXMinutes(10), # <-- Chama o método do controller
                                        width=90, height=45,
                                        font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                        fg_color="#333333", hover_color="#555555")
    addTenMinutesButton.pack(pady=10)

    rmTenMinutesButton = ctk.CTkButton(remove_frame,
                                       text="-10 min",
                                       command=lambda: controller.addXMinutes(-10), # <-- Chama o método do controller
                                       width=90, height=45,
                                       font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                       fg_color="#d11e45", hover_color="#ff0048")
    rmTenMinutesButton.pack(pady=10)

    # ----- THIRTY MINUTES BUTTONS ----- #
    addThirtyMinutesButton = ctk.CTkButton(add_frame,
                                           text="+30 min",
                                           command=lambda: controller.addXMinutes(30), # <-- Chama o método do controller
                                           width=90, height=45,
                                           font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                           fg_color="#333333", hover_color="#555555")
    addThirtyMinutesButton.pack(pady=10)

    rmThirtyMinutesButton = ctk.CTkButton(remove_frame,
                                          text="-30 min",
                                          command=lambda: controller.addXMinutes(-30), # <-- Chama o método do controller
                                          width=90, height=45,
                                          font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                          fg_color="#d11e45", hover_color="#ff0048")
    rmThirtyMinutesButton.pack(pady=10)


def create_action_buttons(action_frame, controller):

    shutdownButton = ctk.CTkButton(action_frame,
                                   text="Shutdown",
                                   command=lambda: controller.scheduleAction('shutdown'), # <-- Chama o método do controller
                                   font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                   height=45, width=180,
                                   fg_color="#6600cc", hover_color="#9d00ff")
    shutdownButton.pack(pady=10)

    sleepButton = ctk.CTkButton(action_frame,
                                text="Sleep / Hibernate",
                                command=lambda: controller.scheduleAction('sleep'), # <-- Chama o método do controller
                                font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                height=45, width=180,
                                fg_color="#2a75bb", hover_color="#3697e1")
    sleepButton.pack(pady=10)

    cancelButton = ctk.CTkButton(action_frame,
                                 text="Cancel Action",
                                 command=controller.cancelAction, # <-- Chama o método do controller
                                 font=('Segoe UI', 14, 'bold'), corner_radius=15,
                                 height=45, width=180,
                                 fg_color="#d11e45", hover_color="#ff0048")
    cancelButton.pack(pady=10)
