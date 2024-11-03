class HashTable:
    def __init__(self, size=100):
        # Initialize the hash table with a fixed size
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        # Simple hash function to convert key to an index
        return hash(key) % self.size

    def insert(self, key, value):
        # Calculate the index for the key
        index = self._hash_function(key)
        
        # Check if key already exists
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return
        
        # If key doesn't exist, append new key-value pair
        self.table[index].append([key, value])

    def get(self, key):
        # Find the index for the key
        index = self._hash_function(key)
        
        # Search for the key in the bucket
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        
        # Raise error if key not found
        raise KeyError(key)

    def remove(self, key):
        # Find the index for the key
        index = self._hash_function(key)
        
        # Find and remove the key
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                return
        
        # Raise error if key not found
        raise KeyError(key)

    def keys(self):
        # Return all keys in the hash table
        all_keys = []
        for bucket in self.table:
            for item in bucket:
                all_keys.append(item[0])
        return all_keys

class ProfileManager:
    def __init__(self, secret_key='default_secret_key'):
        self.secret_key = secret_key
        # Use custom HashTable instead of dictionary
        self.profiles = HashTable()

    def generate_profile_id(self):
        """Custom UUID4 generation"""
        import random
        hex_chars = '0123456789abcdef'
        uuid_parts = [
            ''.join(random.choice(hex_chars) for _ in range(8)),
            ''.join(random.choice(hex_chars) for _ in range(4)),
            '4' + ''.join(random.choice(hex_chars) for _ in range(3)),
            str(random.randint(8, 11)) + ''.join(random.choice(hex_chars) for _ in range(3)),
            ''.join(random.choice(hex_chars) for _ in range(12))
        ]
        return '-'.join(uuid_parts)

    def create_profile_hash(self, profile_id, profile_data):
        """Custom hash generation"""
        hash_value = 0x811c9dc5
        fnv_prime = 0x01000193

        data_str = str(profile_id) + str(profile_data)
        
        for char in data_str:
            hash_value = hash_value ^ ord(char)
            hash_value = (hash_value * fnv_prime) & 0xFFFFFFFF
        
        return hex(hash_value ^ hash(self.secret_key))[2:]

    def create_profile(self, profile_settings):
        # Generate unique ID
        profile_id = self.generate_profile_id()
        
        # Create hash for integrity
        profile_hash = self.create_profile_hash(profile_id, profile_settings)

        # Create profile entry
        profile_entry = {
            'id': profile_id,
            'settings': profile_settings,
            'hash': profile_hash
        }

        # Store the profile in custom hash table
        self.profiles.insert(profile_id, profile_entry)
        return profile_entry

    def get_profile(self, profile_id):
        try:
            # Retrieve profile from hash table
            profile = self.profiles.get(profile_id)

            # Verify profile integrity
            verification_hash = self.create_profile_hash(
                profile['id'], 
                profile['settings']
            )
            
            # Check if hash matches
            if verification_hash != profile['hash']:
                raise ValueError('Profile data has been tampered with')

            return profile['settings']
        except KeyError:
            raise ValueError('Profile not found')

    def update_profile(self, profile_id, new_settings):
        try:
            # Retrieve existing profile
            existing_profile = self.profiles.get(profile_id)

            # Generate new hash with updated settings
            new_hash = self.create_profile_hash(profile_id, new_settings)

            # Update profile
            updated_profile = {
                'id': profile_id,
                'settings': new_settings,
                'hash': new_hash
            }

            # Update in hash table
            self.profiles.insert(profile_id, updated_profile)
            return updated_profile
        except KeyError:
            raise ValueError('Profile not found')

    def list_profiles(self):
        """List all profile IDs"""
        return self.profiles.keys()

# Demonstration remains the same as previous example
def demonstrate_profile_manager():
    profile_manager = ProfileManager('my_secret_key')

    user_profile1 = profile_manager.create_profile({
        'theme': 'dark',
        'notifications': True,
        'language': 'en'
    })

    user_profile2 = profile_manager.create_profile({
        'theme': 'light',
        'notifications': False,
        'language': 'es'
    })

    print("Profile 1 ID:", user_profile1['id'])
    print("Profile 2 ID:", user_profile2['id'])

    try:
        retrieved_profile1 = profile_manager.get_profile(user_profile1['id'])
        print("Retrieved Profile 1:", retrieved_profile1)

        updated_profile = profile_manager.update_profile(user_profile1['id'], {
            'theme': 'light',
            'notifications': False,
            'language': 'fr'
        })

        print("Updated Profile 1:", updated_profile['settings'])

        print("All Profile IDs:", list(profile_manager.list_profiles()))

    except Exception as error:
        print("Error:", str(error))
        
if __name__ == "__main__":
    demonstrate_profile_manager()   