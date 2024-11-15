import os

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]  # Initialize the hash table with empty lists
    
    def hash_function(self, key):
        return hash(key) % self.size  # Compute the hash index for a given key
    
    def insert(self, key, value):
        hash_index = self.hash_function(key)  # Get the index for the key
        for item in self.table[hash_index]:
            if item[0] == key:
                item[1] = value  # Update existing profile if key already exists
                return
        self.table[hash_index].append([key, value])  # Insert new key-value pair
    
    def get(self, key):
        hash_index = self.hash_function(key)  # Get the index for the key
        for item in self.table[hash_index]:
            if item[0] == key:
                return item[1]  # Return the value if key is found
        return None  # Return None if key is not found
    
    def delete(self, key):
        hash_index = self.hash_function(key)  # Get the index for the key
        for i, item in enumerate(self.table[hash_index]):
            if item[0] == key:
                del self.table[hash_index][i]  # Delete the item if key is found
                return True
        return False  # Return False if key is not found
    
    def keys(self):
        return [item[0] for chain in self.table for item in chain]  # Return all keys in the hash table
    
    def items(self):
        return [(item[0], item[1]) for chain in self.table for item in chain]  # Return all key-value pairs

def create_default_profiles_file():
    default_content = "default|work|#FFFFFF|14|120||\n"  # Default profile content
    with open('profiles.txt', 'w') as file:
        file.write(default_content)  # Write default content to profiles.txt
    print("Default profiles.txt file created.")

def load_profiles():
    profiles = HashTable()  # Create a new hash table for profiles
    if not os.path.exists('profiles.txt'):
        create_default_profiles_file()  # Create default file if it doesn't exist

    try:
        with open('profiles.txt', 'r') as file:
            for line in file:
                data = line.strip().split('|')  # Split line into components
                if len(data) == 7:  # Ensure the line has the correct number of components
                    bookmarks = data[5].split(',')  # Split bookmarks
                    accounts = {}
                    for account in data[6].split(','):
                        if ':' in account:
                            service, email = account.split(':')  # Split account into service and email
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
                    profiles.insert(data[0], profile)  # Insert profile into hash table
    except FileNotFoundError:
        print("Error: profiles.txt file not found!")  # Handle file not found error
    except Exception as e:
        print(f"Error loading profiles: {str(e)}")  # Handle other exceptions
    
    return profiles  # Return the loaded profiles

def save_profiles(profiles):
    try:
        with open('profiles.txt', 'w') as file:
            for username, profile in profiles.items():
                bookmarks = ','.join(profile['settings']['bookmarks'])  # Join bookmarks into a string
                accounts = ','.join(f"{service}:{email}" for service, email in profile['settings']['accounts'].items())  # Join accounts into a string
                line = f"{profile['username']}|{profile['settings']['profile_type']}|{profile['settings']['background_color']}|{profile['settings']['font_size']}|{profile['settings']['zoom_level']}|{bookmarks}|{accounts}\n"
                file.write(line)  # Write profile data to file
    except Exception as e:
        print(f"Error saving profiles: {str(e)}")  # Handle exceptions during saving

def update_profile_settings(profile):
    settings = profile["settings"]  # Access the profile settings
    
    print("\nUpdate Profile Settings (type 'same' to keep the current value):")
    
    new_profile_type = input(f"Profile Type [{settings['profile_type']}]: ")
    if new_profile_type.lower() != "same":
        settings["profile_type"] = new_profile_type  # Update profile type if new value is provided

    new_background_color = input(f"Background Color [{settings['background_color']}]: ")
    if new_background_color.lower() != "same":
        settings["background_color"] = new_background_color  # Update background color if new value is provided

    new_font_size = input(f"Font Size [{settings['font_size']}px]: ")
    if new_font_size.lower() != "same":
        try:
            settings["font_size"] = int(new_font_size)  # Update font size if valid input is provided
        except ValueError:
            print("Invalid input for font size. Keeping the current value.")  # Handle invalid input

    new_zoom_level = input(f"Zoom Level [{settings['zoom_level']}%]: ")
    if new_zoom_level.lower() != "same":
        try:
            settings["zoom_level"] = int(new_zoom_level)  # Update zoom level if valid input is provided
        except ValueError:
            print("Invalid input for zoom level. Keeping the current value.")  # Handle invalid input

    new_bookmarks = input(f"Bookmarks [{', '.join(settings['bookmarks'])}]: ")
    if new_bookmarks.lower() != "same":
        settings["bookmarks"] = new_bookmarks.split(',') if new_bookmarks else []  # Update bookmarks if new value is provided

    new_accounts = input("Accounts (e.g., gmail:you@example.com, yahoo:me@example.com) "
                         f"[{', '.join(f'{k}:{v}' for k, v in settings['accounts'].items())}]: ")
    if new_accounts.lower() != "same":
        settings["accounts"] = {}
        for account in new_accounts.split(','):
            if ':' in account:
                service, email = account.split(':')  # Split account into service and email
                settings["accounts"][service.strip()] = email.strip()  # Update accounts

    print("Profile settings updated.")  # Confirmation message

def show_profile_details(profile):
    print("\nProfile Details:")
    print(f"Username: {profile['username']}")  # Display username
    settings = profile['settings']
    print(f"Profile Type: {settings['profile_type']}")  # Display profile type
    print(f"Background Color: {settings['background_color']}")  # Display background color
    print(f"Font Size: {settings['font_size']}px")  # Display font size
    print(f"Zoom Level: {settings['zoom_level']}%")  # Display zoom level
    print(f"Bookmarks: {', '.join(settings['bookmarks'])}")  # Display bookmarks
    print(f"Connected Accounts: {', '.join(settings['accounts'].keys())}")  # Display connected accounts

def add_account(profiles):
    username = input("Enter the username for the new account: ")  # Prompt for new account username
    
    new_profile = {
        "userID": username,
        "username": username,
        "settings": {
            "profile_type": "default",  # Default profile type
            "background_color": "#FFFFFF",  # Default background color
            "font_size": 14,  # Default font size
            "zoom_level": 100,  # Default zoom level
            "bookmarks": [],  # Default bookmarks
            "accounts": {},  # Default accounts
            "passwords": {}  # Default passwords
        }
    }
    
    profiles.insert(username, new_profile)  # Insert new profile into hash table
    print(f"Account '{username}' added successfully with default settings.")  # Confirmation message

def main():
    profiles = load_profiles()  # Load profiles from file
    
    if not profiles.keys():
        print("No profiles loaded. Exiting...")  # Exit if no profiles are found
        return
    
    while True:
        print("\nSelect an Account:")
        usernames = profiles.keys()  # Get list of usernames
        for idx, username in enumerate(usernames, start=1):
            print(f"{idx}. {username}")  # Display usernames
        print(f"{len(usernames) + 1}. Add Account")  # Option to add account
        print(f"{len(usernames) + 2}. Exit")  # Option to exit

        choice = input("\nEnter your choice: ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(usernames):
            selected_profile = profiles.get(usernames[int(choice) - 1])  # Get selected profile
            while True:
                print(f"\nSelected Account: {selected_profile['username']}")
                print("1. Switch Account")  # Option to switch account
                print("2. Settings")  # Option to view settings
                print("3. Exit")  # Option to exit
                
                sub_choice = input("\nEnter your choice (1-3): ")
                
                if sub_choice == '1':
                    break  # Break to select another account
                elif sub_choice == '2':
                    show_profile_details(selected_profile)  # Show profile details
                    edit_choice = input("Type 'edit' to change settings: ")
                    if edit_choice.lower() == 'edit':
                        update_profile_settings(selected_profile)  # Update profile settings
                    save_profiles(profiles)  # Save profiles after editing
                elif sub_choice == '3':
                    print("Goodbye!")  # Exit message
                    return
                else:
                    print("Invalid choice. Please try again.")  # Handle invalid choice
        elif choice == str(len(usernames) + 1):
            add_account(profiles)  # Add new account
            save_profiles(profiles)  # Save profiles after adding
        elif choice == str(len(usernames) + 2):
            print("Goodbye!")  # Exit message
            break
        else:
            print("Invalid choice. Please try again.")  # Handle invalid choice

if __name__ == "__main__":
    main()  # Start the program