class Tab:
    def __init__(self, url):
        self.url = url
        self.content = None

    def load_content(self):
        # Code to load the content of the tab
        self.content = "Example content"

    def save_state(self):
        # Code to save the state of the tab
        pass