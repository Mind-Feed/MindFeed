import customtkinter as ctk
from .settings_panel import SettingsPanel
from .bookmarks_manager import BookmarksManager
from browser import BrowserWindow

class MainWindow(ctk.CTk):
    def __init__(self, storage_manager):
        super().__init__()
        self.title("Sage Browser")
        self.geometry("800x600")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.browser_window = BrowserWindow(storage_manager)
        self.settings_panel = SettingsPanel(self, self.browser_window)
        self.bookmarks_manager = BookmarksManager(self, self.browser_window)

        self.content_area = None

        self.create_widgets()

    def create_widgets(self):
        # Create the main UI elements using CustomTkinter widgets
        self.sidebar = ctk.CTkFrame(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.settings_button = ctk.CTkButton(self.sidebar, text="Settings", command=self.show_settings)
        self.settings_button.grid(row=0, column=0, padx=10, pady=10)

        self.bookmarks_button = ctk.CTkButton(self.sidebar, text="Bookmarks", command=self.show_bookmarks)
        self.bookmarks_button.grid(row=1, column=0, padx=10, pady=10)

        self.content_area = ctk.CTkFrame(self)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_settings(self):
        if self.content_area:
            self.content_area.destroy()
            
        self.content_area = self.settings_panel
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def show_bookmarks(self):
        if self.content_area:
            self.content_area.destroy()
            
        self.content_area = self.bookmarks_manager
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)