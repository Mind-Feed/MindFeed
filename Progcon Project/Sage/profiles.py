from data_structures import HashTable

class UserProfile:
    def __init__(self, username):
        self.username = username
        self.preferences = {
            'background_image': 'default.jpg',
            'font_size': 12,
            'theme': 'light'
        }
        self.pinned_tabs = []

class ProfileManager:
    def __init__(self):
        self.profiles = {}  # key: username, value: UserProfile
        self.current_profile = None

    def add_profile(self, username):
        profile = UserProfile(username)
        self.profiles[username] = profile
        return profile

    def get_profile(self, username):
        return self.profiles.get(username)

    def switch_profile(self, username):
        profile = self.get_profile(username)
        if profile:
            self.current_profile = profile
            return profile
        return None

    def save_pinned_tabs(self, tabs):
        if self.current_profile:
            self.current_profile.pinned_tabs = tabs
