from ui import BrowserUI
from profiles import ProfileManager
from bookmarks import BookmarkManager

class Browser:
    def __init__(self):
        self.profile_manager = ProfileManager()
        self.bookmark_manager = BookmarkManager()
        self.ui = None

    def initialize(self):
        self.ui = BrowserUI(self)  # Pass browser instance to UI
        self.ui.mainloop()

if __name__ == "__main__":
    browser = Browser()
    browser.initialize() 