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

def create_profile_hash(self, profile_id, profile_data):
        """Custom hash generation"""
        hash_value = 0x811c9dc5
        fnv_prime = 0x01000193

        data_str = str(profile_id) + str(profile_data)
        
        for char in data_str:
            hash_value = hash_value ^ ord(char)
            hash_value = (hash_value * fnv_prime) & 0xFFFFFFFF
        
        return hex(hash_value ^ hash(self.secret_key))[2:]
    
