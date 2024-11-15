from profile import Profile

class StorageManager:
    def __init__(self):
        self.profiles = {}
        self.bookmarks = {}
        self.history = []

    def save_profile(self, profile):
        self.profiles[profile.id] = profile
        profile.save(f"{profile.id}.json")

    def load_profile(self, profile_id):
        if profile_id in self.profiles:
            return self.profiles[profile_id]
        else:
            profile = Profile.load(f"{profile_id}.json")
            self.profiles[profile_id] = profile
            return profile

    def add_bookmark(self, bookmark):
        self.bookmarks[bookmark.url] = bookmark

    def search_bookmarks(self, query):
        return [bookmark for url, bookmark in self.bookmarks.items() if query in url]

    def add_history_entry(self, timestamp, url):
        self.history.append((timestamp, url))

    def get_history(self, start_time, end_time):
        return [entry for entry in self.history if start_time <= entry[0] <= end_time]