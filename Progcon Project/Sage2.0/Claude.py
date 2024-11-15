import os

def create_default_profiles_file():
    """Create a default profiles.txt file with initial content."""
    default_content = (
        "dafault|work|#FFFFFF|14|120||\n"
    )
    with open('profiles.txt', 'w') as file:
        file.write(default_content)
    print("Default profiles.txt file created.")

def load_profiles():
    profiles = {}
    if not os.path.exists('profiles.txt'):
        create_default_profiles_file()  # Create the file if it doesn't exist

    try:
        with open('profiles.txt', 'r') as file:
            for line in file:
                # Split the line into components
                data = line.strip().split('|')
                if len(data) == 7:
                    # Convert bookmarks string to list
                    bookmarks = data[5].split(',')
                    
                    # Convert accounts string to dictionary
                    accounts = {}
                    for account in data[6].split(','):
                        if ':' in account:
                            service, email = account.split(':')
                            accounts[service] = email
                    
                    # Create profile dictionary with username as key
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
                    profiles[data[0]] = profile
    except FileNotFoundError:
        print("Error: profiles.txt file not found!")
    except Exception as e:
        print(f"Error loading profiles: {str(e)}")
    
    return profiles

def save_profiles(profiles):
    try:
        with open('profiles.txt', 'w') as file:
            for profile in profiles.values():
                # Prepare the line to write
                bookmarks = ','.join(profile['settings']['bookmarks'])
                accounts = ','.join(f"{service}:{email}" for service, email in profile['settings']['accounts'].items())
                line = f"{profile['username']}|{profile['settings']['profile_type']}|{profile['settings']['background_color']}|{profile['settings']['font_size']}|{profile['settings']['zoom_level']}|{bookmarks}|{accounts}\n"
                file.write(line)
    except Exception as e:
        print(f"Error saving profiles: {str(e)}")

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

def update_profile_settings(profile):
    # Update profile settings logic (same as before)
    pass

def add_account(profiles):
    username = input("Enter the username for the new account: ")
    
    # Default settings for the new account 
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
    
    profiles[username] = new_profile
    print(f"Account '{username}' added successfully with default settings.")

def main():
    # Load profiles from file
    profiles = load_profiles()
    
    if not profiles:
        print("No profiles loaded. Exiting...")
        return
    
    while True:
        print("\nSelect an Account:")
        for username in profiles:
            print(f"{username}")
        print(f"{len(profiles) + 1}. Add Account")
        print(f"{len(profiles) + 2}. Exit")

        choice = input("\nEnter your choice: ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            selected_profile = list(profiles.values())[int(choice) - 1]
            while True:
                print(f"\nSelected Account: {selected_profile['username']}")
                print("1. Switch Account")
                print("2. Settings")
                print("3. Exit")
                
                sub_choice = input("\nEnter your choice (1-3): ")
                
                if sub_choice == '1':
                    break  # Go back to account selection
                elif sub_choice == '2':
                    show_profile_details(selected_profile)
                    update_profile_settings(selected_profile)
                    save_profiles(profiles)  # Save changes to the file
                elif sub_choice == '3':
                    print("Goodbye!")
                    return
                else:
                    print("Invalid choice. Please try again.")
        elif choice == str(len(profiles) + 1):
            add_account(profiles)  # Call the function to add a new account
            save_profiles(profiles)  # Save the updated profiles to the file
        elif choice == str(len(profiles) + 2):
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()