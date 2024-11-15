import customtkinter as ctk

class TabButton(ctk.CTkFrame):
    def __init__(self, master, title="New Tab", on_close=None, on_pin=None, on_click=None, is_pinned=False):
        super().__init__(master)
        
        # Store callbacks
        self.on_click = on_click
        self.is_active = False
        
        # Make the entire frame clickable
        self.bind("<Button-1>", self._on_click)
        
        # Container frame for better organization
        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True)
        self.content.bind("<Button-1>", self._on_click)
        
        # Title label
        self.title_label = ctk.CTkLabel(self.content, text=title)
        self.title_label.pack(side="left", padx=5)
        self.title_label.bind("<Button-1>", self._on_click)
        
        # Button container
        self.button_container = ctk.CTkFrame(self.content)
        self.button_container.pack(side="right", padx=2)
        
        # Pin button
        self.is_pinned = is_pinned
        self.pin_button = ctk.CTkButton(
            self.button_container,
            text="📌" if not is_pinned else "📍",
            width=20,
            height=20,
            command=lambda: on_pin(self) if on_pin else None
        )
        self.pin_button.pack(side="left", padx=2)
        
        # Close button
        self.close_button = ctk.CTkButton(
            self.button_container,
            text="×",
            width=20,
            height=20,
            command=lambda: on_close(self) if on_close else None
        )
        self.close_button.pack(side="left", padx=2)
        
        # Visual feedback
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.content.bind("<Enter>", self._on_enter)
        self.content.bind("<Leave>", self._on_leave)
        self.title_label.bind("<Enter>", self._on_enter)
        self.title_label.bind("<Leave>", self._on_leave)
    
    def set_active(self, active):
        self.is_active = active
        if active:
            self.configure(fg_color=("gray80", "gray20"))
            self.content.configure(fg_color=("gray80", "gray20"))
        else:
            self.configure(fg_color=("gray70", "gray30"))
            self.content.configure(fg_color=("gray70", "gray30"))
            
    def _on_click(self, event=None):
        if self.on_click:
            self.on_click(self)
            
    def _on_enter(self, event=None):
        if not self.is_active:
            self.configure(fg_color=("gray75", "gray25"))
            self.content.configure(fg_color=("gray75", "gray25"))
        
    def _on_leave(self, event=None):
        if not self.is_active:
            self.configure(fg_color=("gray70", "gray30"))
            self.content.configure(fg_color=("gray70", "gray30"))

class SidebarButton(ctk.CTkButton):
    def __init__(self, master, text, **kwargs):
        super().__init__(
            master,
            text=text,
            width=150,
            height=40,
            corner_radius=10,
            **kwargs
        )

class ProfileDialog(ctk.CTkToplevel):
    def __init__(self, parent, profile_manager, on_switch=None):
        super().__init__(parent)
        self.title("Profile Management")
        self.geometry("400x300")
        
        self.profile_manager = profile_manager
        self.on_switch = on_switch
        
        # Create widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Profile creation frame
        create_frame = ctk.CTkFrame(self)
        create_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(create_frame, text="Create New Profile").pack()
        
        self.username_entry = ctk.CTkEntry(create_frame, placeholder_text="Username")
        self.username_entry.pack(pady=5)
        
        ctk.CTkButton(
            create_frame,
            text="Create Profile",
            command=self.create_profile
        ).pack(pady=5)
        
        # Profile list frame
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ctk.CTkLabel(list_frame, text="Switch Profile").pack()
        
        self.profile_list = ctk.CTkScrollableFrame(list_frame)
        self.profile_list.pack(fill="both", expand=True, pady=5)
        
        self.update_profile_list()
        
    def create_profile(self):
        username = self.username_entry.get()
        
        if username:
            profile = self.profile_manager.add_profile(username)
            self.update_profile_list()
            self.username_entry.delete(0, 'end')
            
    def update_profile_list(self):
        # Clear existing buttons
        for widget in self.profile_list.winfo_children():
            widget.destroy()
            
        # Add profile buttons
        for username, profile in self.profile_manager.profiles.items():
            btn = ctk.CTkButton(
                self.profile_list,
                text=username,
                command=lambda u=username: self.switch_profile(u)
            )
            btn.pack(fill="x", pady=2)
                
    def switch_profile(self, username):
        profile = self.profile_manager.switch_profile(username)
        if profile and self.on_switch:
            self.on_switch(profile)