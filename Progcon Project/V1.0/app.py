import customtkinter as ctk
from ui.main_window import MainWindow
from storage import StorageManager

if __name__ == "__main__":
    ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

    storage_manager = StorageManager()
    main_window = MainWindow(storage_manager)
    main_window.mainloop()