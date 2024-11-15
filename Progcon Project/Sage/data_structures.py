class HashTable:
    def __init__(self, size=100):
        self.table = [[] for _ in range(size)]
        self.size = size

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value)) 