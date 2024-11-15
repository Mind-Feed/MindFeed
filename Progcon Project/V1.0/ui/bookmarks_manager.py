# ui/bookmarks_manager.py
import customtkinter as ctk

class BookmarksManager(ctk.CTkFrame):
    def __init__(self, parent, browser_window):
        super().__init__(parent)
        self.browser_window = browser_window
        self.create_widgets()

    def create_widgets(self):
        # Create the bookmarks manager UI elements using CustomTkinter widgets
        self.title_label = ctk.CTkLabel(self, text="Bookmarks", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        self.bookmarks_list = ctk.CTkTextbox(self)
        self.bookmarks_list.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")