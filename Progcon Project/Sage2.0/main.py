import os

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]
    
    def hash_function(self, key):
        return hash(key) % self.size
    
    def insert(self, key, value):
        hash_index = self.hash_function(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                item[1] = value  # Update existing profile
                return
        self.table[hash_index].append([key, value])
    
    def get(self, key):
        hash_index = self.hash_function(key)
        for item in self.table[hash_index]:
            if item[0] == key:
                return item[1]
        return None
    
    def delete(self, key):
        hash_index = self.hash_function(key)
        for i, item in enumerate(self.table[hash_index]):
            if item[0] == key:
                del self.table[hash_index][i]
                return True
        return False
    
    def keys(self):
        return [item[0] for chain in self.table for item in chain]
    
    def items(self):
        return [(item[0], item[1]) for chain in self.table for item in chain]

def create_default_profiles_file():
    default_content = "default|work|#FFFFFF|14|120||\n"
    with open('profiles.txt', 'w') as file:
        file.write(default_content)
    print("Default profiles.txt file created.")

def load_profiles():
    profiles = HashTable()
    if not os.path.exists('profiles.txt'):
        create_default_profiles_file()

    try:
        with open('profiles.txt', 'r') as file:
            for line in file:
                data = line.strip().split('|')
                if len(data) == 7:
                    bookmarks = data[5].split(',')
                    accounts = {}
                    for account in data[6].split(','):
                        if ':' in account:
                            service, email = account.split(':')
                            accounts[service] = email
                    profile = {
                        "userID": data[0],
                        "username": data[0],
                        "settings": {
                            "profile_type": data[1],
                            "background_color": data[2],
                            "font_size": int(data[3]),
                            "zoom_level": int(data[4]),
                            "bookmarks": bookmarks,
                            "accounts": accounts,
                            "passwords": {}
                        }
                    }
                    profiles.insert(data[0], profile)
    except FileNotFoundError:
        print("Error: profiles.txt file not found!")
    except Exception as e:
        print(f"Error loading profiles: {str(e)}")
    
    return profiles

def save_profiles(profiles):
    try:
        with open('profiles.txt', 'w') as file:
            for username, profile in profiles.items():
                bookmarks = ','.join(profile['settings']['bookmarks'])
                accounts = ','.join(f"{service}:{email}" for service, email in profile['settings']['accounts'].items())
                line = f"{profile['username']}|{profile['settings']['profile_type']}|{profile['settings']['background_color']}|{profile['settings']['font_size']}|{profile['settings']['zoom_level']}|{bookmarks}|{accounts}\n"
                file.write(line)
    except Exception as e:
        print(f"Error saving profiles: {str(e)}")

def update_profile_settings(profile):
    settings = profile["settings"]
    
    print("\nUpdate Profile Settings (type 'same' to keep the current value):")
    
    new_profile_type = input(f"Profile Type [{settings['profile_type']}]: ")
    if new_profile_type.lower() != "same":
        settings["profile_type"] = new_profile_type

    new_background_color = input(f"Background Color [{settings['background_color']}]: ")
    if new_background_color.lower() != "same":
        settings["background_color"] = new_background_color

    new_font_size = input(f"Font Size [{settings['font_size']}px]: ")
    if new_font_size.lower() != "same":
        try:
            settings["font_size"] = int(new_font_size)
        except ValueError:
            print("Invalid input for font size. Keeping the current value.")

    new_zoom_level = input(f"Zoom Level [{settings['zoom_level']}%]: ")
    if new_zoom_level.lower() != "same":
        try:
            settings["zoom_level"] = int(new_zoom_level)
        except ValueError:
            print("Invalid input for zoom level. Keeping the current value.")

    new_bookmarks = input(f"Bookmarks [{', '.join(settings['bookmarks'])}]: ")
    if new_bookmarks.lower() != "same":
        settings["bookmarks"] = new_bookmarks.split(',') if new_bookmarks else []

    new_accounts = input("Accounts (e.g., gmail:you@example.com, yahoo:me@example.com) "
                         f"[{', '.join(f'{k}:{v}' for k, v in settings['accounts'].items())}]: ")
    if new_accounts.lower() != "same":
        settings["accounts"] = {}
        for account in new_accounts.split(','):
            if ':' in account:
                service, email = account.split(':')
                settings["accounts"][service.strip()] = email.strip()

    print("Profile settings updated.")

def show_profile_details(profile):
    print("\nProfile Details:")
    print(f"Username: {profile['username']}")
    settings = profile['settings']
    print(f"Profile Type: {settings['profile_type']}")
    print(f"Background Color: {settings['background_color']}")
    print(f"Font Size: {settings['font_size']}px")
    print(f"Zoom Level: {settings['zoom_level']}%")
    print(f"Bookmarks: {', '.join(settings['bookmarks'])}")
    print(f"Connected Accounts: {', '.join(settings['accounts'].keys())}")

def add_account(profiles):
    username = input("Enter the username for the new account: ")
    
    new_profile = {
        "userID": username,
        "username": username,
        "settings": {
            "profile_type": "default",
            "background_color": "#FFFFFF",
            "font_size": 14,
            "zoom_level": 100,
            "bookmarks": [],
            "accounts": {},
            "passwords": {}
        }
    }
    
    profiles.insert(username, new_profile)
    print(f"Account '{username}' added successfully with default settings.")

def main():
    profiles = load_profiles()
    
    if not profiles.keys():
        print("No profiles loaded. Exiting...")
        create_default_profiles_file()
        return
    
    while True:
        print("\nSelect an Account:")
        usernames = profiles.keys()
        for idx, username in enumerate(usernames, start=1):
            print(f"{idx}. {username}")
        print(f"{len(usernames) + 1}. Add Account")
        print(f"{len(usernames) + 2}. Exit")

        choice = input("\nEnter your choice: ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(usernames):
            selected_profile = profiles.get(usernames[int(choice) - 1])
            while True:
                print(f"\nSelected Account: {selected_profile['username']}")
                print("1. Switch Account")
                print("2. Settings")
                print("3. Delete Account")
                print("4. Exit")
                
                sub_choice = input("\nEnter your choice (1-4): ")
                
                if sub_choice == '1':
                    break
                elif sub_choice == '2':
                    show_profile_details(selected_profile)
                    edit_choice = input("Type 'edit' to change settings: ")
                    if edit_choice.lower() == 'edit':
                        update_profile_settings(selected_profile)
                    save_profiles(profiles)
                elif sub_choice == '3':
                    confirm = input("Are you sure you want to delete this account? (yes/no): ")
                    if confirm.lower() == 'yes':
                        profiles.delete(selected_profile['username'])
                        print(f"Account '{selected_profile['username']}' deleted successfully.")
                        save_profiles(profiles)
                        break
                elif sub_choice == '4':
                    print("Goodbye!")
                    return
                else:
                    print("Invalid choice. Please try again.")
        elif choice == str(len(usernames) + 1):
            add_account(profiles)
            save_profiles(profiles)
        elif choice == str(len(usernames) + 2):
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
