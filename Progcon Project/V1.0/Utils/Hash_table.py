class HashTable:
    def __init__(self, capacity=1024):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]

    def __getitem__(self, key):
        index = self.hash(key)
        for pair in self.buckets[index]:
            if pair[0] == key:
                return pair[1]
        raise KeyError(key)

    def __setitem__(self, key, value):
        index = self.hash(key)
        for pair in self.buckets[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.buckets[index].append([key, value])

    def __contains__(self, key):
        index = self.hash(key)
        for pair in self.buckets[index]:
            if pair[0] == key:
                return True
        return False

    def hash(self, key):
        return hash(key) % self.capacity