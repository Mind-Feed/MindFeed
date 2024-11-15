from tab import Tab

class BrowserWindow:
    def __init__(self, storage_manager):
        self.storage_manager = storage_manager
        self.tabs = []
        self.active_tab = None

    def set_profile(self, profile):
        self.profile = profile

    def create_tab(self, url):
        tab = Tab(url)
        self.tabs.append(tab)
        self.set_active_tab(tab)
        return tab

    def set_active_tab(self, tab):
        if self.active_tab:
            self.active_tab.save_state()
        self.active_tab = tab
        tab.load_content()

    def close_tab(self, tab):
        self.tabs.remove(tab)
        if tab == self.active_tab:
            self.set_active_tab(self.tabs[-1] if self.tabs else None)