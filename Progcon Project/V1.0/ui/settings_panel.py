import customtkinter as ctk

class SettingsPanel(ctk.CTkFrame):
    def __init__(self, parent, browser_window):
        super().__init__(parent)
        self.browser_window = browser_window
        self.create_widgets()

    def create_widgets(self):
        # Create the settings panel UI elements using CustomTkinter widgets
        self.title_label = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        self.theme_option_menu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"])
        self.theme_option_menu.grid(row=1, column=0, padx=20, pady=10)

        self.font_size_slider = ctk.CTkSlider(self, from_=12, to=24, number_of_steps=6)
        self.font_size_slider.grid(row=2, column=0, padx=20, pady=10)

