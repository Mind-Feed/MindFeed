import customtkinter as ctk
from ui_components import TabButton, SidebarButton, ProfileDialog
from tab_manager import TabManager

class BrowserUI(ctk.CTk):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser
        self.title("Browser")
        self.geometry("1200x800")
        
        # Create managers
        self.tab_manager = TabManager(browser)
        
        # Create layout
        self.create_main_content()
        self.create_sidebar()
        self.create_tab_bar()
        
        # Add initial tab
        self.add_new_tab()
        
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=200)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        buttons = [
            ("Profiles", self.show_profiles),
            ("Bookmarks", self.show_bookmarks)
        ]
        
        for text, command in buttons:
            btn = SidebarButton(sidebar, text=text, command=command)
            btn.pack(pady=5, padx=10)
            
    def create_tab_bar(self):
        self.tab_frame = ctk.CTkFrame(self)
        self.tab_frame.pack(fill="x", padx=10, pady=(10,0))
        
        # Create separate frames for pinned and unpinned tabs
        self.pinned_frame = ctk.CTkFrame(self.tab_frame, width=150)
        self.pinned_frame.pack(side="left", fill="y", padx=(0,10))
        self.pinned_frame.pack_propagate(False)
        
        self.unpinned_frame = ctk.CTkFrame(self.tab_frame)
        self.unpinned_frame.pack(side="left", fill="x", expand=True)
        
        # New tab button
        self.new_tab_btn = ctk.CTkButton(
            self.tab_frame,
            text="+",
            width=30,
            command=self.add_new_tab
        )
        self.new_tab_btn.pack(side="right", padx=5)
        
    def create_main_content(self):
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.tab_contents = {}
        
    def add_new_tab(self, title="New Tab"):
        # Create tab in unpinned frame by default
        tab = TabButton(
            self.unpinned_frame,
            title=title,
            on_close=self.close_tab,
            on_pin=self.toggle_pin,
            on_click=self.switch_tab
        )
        tab.pack(side="left", padx=2)
        
        # Create content for this tab
        content = ctk.CTkTextbox(self.content_frame, wrap="word")
        self.tab_contents[tab] = content
        
        self.switch_tab(tab)
        return tab
        
    def switch_tab(self, tab):
        # Hide all tab contents
        for widget in self.tab_contents.values():
            widget.pack_forget()
        
        # Show selected tab's content
        if tab in self.tab_contents:
            self.tab_contents[tab].pack(fill="both", expand=True)
            
        # Update visual state of all tabs
        for t in self.tab_contents.keys():
            if t == tab:
                t.set_active(True)
            else:
                t.set_active(False)
                
    def toggle_pin(self, tab):
        # Store the content and its reference
        content = self.tab_contents[tab]
        old_content = content.get("1.0", "end-1c")
        
        if tab.is_pinned:
            # Move to unpinned frame
            tab.pack_forget()
            # Create new tab in unpinned frame
            new_tab = TabButton(
                self.unpinned_frame,
                title=tab.title_label.cget("text"),
                on_close=self.close_tab,
                on_pin=self.toggle_pin,
                on_click=self.switch_tab,
                is_pinned=False
            )
            new_tab.pack(side="left", padx=2, pady=0)
            self.tab_manager.unpin_tab(new_tab)
            
            # Keep the same content widget, just reassign it to new tab
            del self.tab_contents[tab]
            self.tab_contents[new_tab] = content
            tab.destroy()
            
            self.switch_tab(new_tab)
        else:
            # Move to pinned frame
            tab.pack_forget()
            # Create new tab in pinned frame
            new_tab = TabButton(
                self.pinned_frame,
                title=tab.title_label.cget("text"),
                on_close=self.close_tab,
                on_pin=self.toggle_pin,
                on_click=self.switch_tab,
                is_pinned=True
            )
            new_tab.pack(side="top", padx=2, pady=2, fill="x")
            self.tab_manager.pin_tab(new_tab)
            
            # Keep the same content widget, just reassign it to new tab
            del self.tab_contents[tab]
            self.tab_contents[new_tab] = content
            tab.destroy()
            
            self.switch_tab(new_tab)
        
    def close_tab(self, tab):
        if tab in self.tab_contents:
            self.tab_contents[tab].destroy()
            del self.tab_contents[tab]
        
        tab.destroy()
        
        if not self.tab_contents:
            self.add_new_tab()
            
    def show_profiles(self):
        ProfileDialog(
            self,
            self.browser.profile_manager,
            on_switch=self.handle_profile_switch
        )
        
    def handle_profile_switch(self, profile):
        # Save current pinned tabs to old profile
        if self.browser.profile_manager.current_profile:
            pinned_tabs = [
                {"title": tab.title_label.cget("text"),
                 "content": self.tab_contents[tab].get("1.0", "end-1c")}
                for tab in self.tab_contents.keys()
                if tab.is_pinned
            ]
            self.browser.profile_manager.save_pinned_tabs(pinned_tabs)
        
        # Clear existing tabs
        for tab in list(self.tab_contents.keys()):
            self.close_tab(tab)
        
        # Load pinned tabs from new profile
        for tab_data in profile.pinned_tabs:
            tab = self.add_new_tab(title=tab_data["title"])
            self.tab_contents[tab].insert("1.0", tab_data["content"])
            self.toggle_pin(tab)
        
    def show_bookmarks(self):
        # Implement bookmark view
        pass
