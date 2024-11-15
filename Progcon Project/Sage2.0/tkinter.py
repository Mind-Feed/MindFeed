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
    profiles = []
    if not os.path.exists('profiles.txt'):
        create_default_profiles_file()  # Create the file if it doesn't exist

    try:
        with open('profiles.txt', 'r') as file:
            for line in file:
                # Split the line into components
                data = line.strip().split('|')
                if len(data) == 7:  # Updated to match actual number of fields
                    # Convert bookmarks string to list
                    bookmarks = data[5].split(',')
                    
                    # Convert accounts string to dictionary
                    accounts = {}
                    for account in data[6].split(','):
                        if ':' in account:
                            service, email = account.split(':')
                            accounts[service] = email
                    
                    # Create profile dictionary with username as userID
                    profile = {
                        "userID": data[0],  # Using username as userID
                        "username": data[0],
                        "settings": {
                            "profile_type": data[1],
                            "background_color": data[2],
                            "font_size": int(data[3]),
                            "zoom_level": int(data[4]),
                            "bookmarks": bookmarks,
                            "accounts": accounts,
                            "passwords": {}  # Empty for security
                        }
                    }
                    profiles.append(profile)
    except FileNotFoundError:
        print("Error: profiles.txt file not found!")
        return []
    except Exception as e:
        print(f"Error loading profiles: {str(e)}")
        return []
    
    return profiles

def save_profiles(profiles):
    try:
        with open('profiles.txt', 'w') as file:
            for profile in profiles:
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
    print("\nUpdate Profile Settings:")
    new_profile_type = input("Enter new profile type (or type 'same' to keep current): ")
    if new_profile_type != 'same':
        profile['settings']['profile_type'] = new_profile_type

    new_background_color = input("Enter new background color (or type 'same' to keep current): ")
    if new_background_color != 'same':
        profile['settings']['background_color'] = new_background_color

    new_font_size_input = input("Enter new font size (or type 'same' to keep current): ")
    if new_font_size_input.lower() != 'same':
        new_font_size = int(new_font_size_input)
        profile['settings']['font_size'] = new_font_size

    new_zoom_level_input = input("Enter new zoom level (or type 'same' to keep current): ")
    if new_zoom_level_input.lower() != 'same':
        new_zoom_level = int(new_zoom_level_input)
        profile['settings']['zoom_level'] = new_zoom_level
    
    # Update bookmarks
    print("Choose an option:")
    print("1. Add Bookmark")
    print("2. Delete All Bookmarks")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        bookmarks_input = input("Enter new bookmarks (comma-separated): ")
        profile['settings']['bookmarks'].extend(bookmarks_input.split(','))
    elif choice == '2':
        profile['settings']['bookmarks'] = []
    else:
        print("Invalid choice. No changes made.")
    
    # Update accounts
    accounts_input = input("Enter new accounts (service:email, comma-separated): ")
    accounts = {}
    for account in accounts_input.split(','):
        if ':' in account:
            service, email = account.split(':')
            accounts[service] = email
    profile['settings']['accounts'] = accounts

    print("\nProfile settings updated successfully!")

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
    
    profiles.append(new_profile)
    print(f"Account '{username}' added successfully with default settings.")

def main():
    # Load profiles from file
    profiles = load_profiles()
    
    if not profiles:
        print("No profiles loaded. Exiting...")
        return
    
    while True:
        print("\nSelect an Account:")
        for index, profile in enumerate(profiles):
            print(f"{index + 1}. {profile['username']}")
        print(f"{len(profiles) + 1}. Add Account")
        print(f"{len(profiles) + 2}. Exit")

        choice = input("\nEnter your choice: ")
        
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            selected_profile = profiles[int(choice) - 1]
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
