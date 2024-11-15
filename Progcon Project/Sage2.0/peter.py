import pickle

class ProfileManager:
    def __init__(self, filename="profiles.pkl"):
        self.filename = filename
        self.profiles = self.load_profiles()

    def add_profile(self, profile_name, profile_data):
        """Adds a new profile to the profiles dictionary and saves it."""
        if profile_name in self.profiles:
            print(f"Profile '{profile_name}' already exists. Choose a different name.")
            return
        
        self.profiles[profile_name] = profile_data
        self.save_profiles()
        print(f"Profile '{profile_name}' added successfully.")

    def choose_profile(self, profile_name):
        """Retrieves the specified profile's data if it exists."""
        return self.profiles.get(profile_name, f"Profile '{profile_name}' does not exist.")

    def save_profiles(self):
        """Saves all profiles to a file."""
        with open(self.filename, "wb") as file:
            pickle.dump(self.profiles, file)

    def load_profiles(self):
        """Loads profiles from a file, if available."""
        try:
            with open(self.filename, "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {}

# Usage example:
manager = ProfileManager()
manager.add_profile("User1", {"age": 25, "email": "user1@example.com", "preferences": {"theme": "dark"}})
print(manager.choose_profile("User1"))  # Should print User1's profile data