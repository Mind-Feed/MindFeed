class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def get(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        return None

# Create hash table and add animal examples
animal_table = HashTable()

# Insert examples of different animal types
animal_table.insert("mammals", ["Lion", "Elephant", "Dolphin"])
animal_table.insert("fish", ["Salmon", "Tuna", "Shark"]) 
animal_table.insert("reptiles", ["Snake", "Turtle", "Lizard"])

# Print the animals
print("Mammals:", animal_table.get("mammals"))
print("Fish:", animal_table.get("fish"))
print("Reptiles:", animal_table.get("reptiles"))
