class Profile:
    def __init__(self, profile_id, settings, bookmarks, history):
        self.id = profile_id
        self.settings = settings
        self.bookmarks = bookmarks
        self.history = history

    def save(self, file_path):
        with open(file_path, "w") as f:
            f.write(f"{{\"id\": \"{self.id}\", \"settings\": {self.settings}, \"bookmarks\": {self.bookmarks}, \"history\": {self.history}}}")

    @classmethod
    def load(cls, file_path):
        with open(file_path, "r") as f:
            data = eval(f.read())
            return cls(**data)