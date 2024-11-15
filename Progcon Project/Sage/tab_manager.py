from datetime import datetime
import json

class Tab:
    def __init__(self, title="New Tab", content="", is_pinned=False):
        self.title = title
        self.content = content
        self.is_pinned = is_pinned
        self.timestamp = datetime.now()

class TabManager:
    def __init__(self, browser):
        self.browser = browser
        self.tabs = []
        self.pinned_tabs = []

    def add_tab(self, title="New Tab", content="", is_pinned=False):
        tab = Tab(title, content, is_pinned)
        if is_pinned:
            self.pinned_tabs.append(tab)
            self.save_pinned_tabs()
        else:
            self.tabs.append(tab)
        return tab

    def pin_tab(self, tab):
        if tab not in self.pinned_tabs:
            self.pinned_tabs.append(tab)

    def unpin_tab(self, tab):
        if tab in self.pinned_tabs:
            self.pinned_tabs.remove(tab)

    def save_pinned_tabs(self):
        pinned_data = [{
            'title': tab.title,
            'content': tab.content,
            'timestamp': tab.timestamp.isoformat()
        } for tab in self.pinned_tabs]
        
        with open('pinned_tabs.json', 'w') as f:
            json.dump(pinned_data, f)

    def load_pinned_tabs(self):
        try:
            with open('pinned_tabs.json', 'r') as f:
                pinned_data = json.load(f)
                for data in pinned_data:
                    self.add_tab(
                        title=data['title'],
                        content=data['content'],
                        is_pinned=True
                    )
        except FileNotFoundError:
            pass 