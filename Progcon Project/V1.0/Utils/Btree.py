class BTreeNode:
    def __init__(self, order):
        self.order = order
        self.keys = []
        self.children = []

    def insert(self, key, value):
        # Implementation of the B-tree insert operation
        pass

    def search(self, key):
        # Implementation of the B-tree search operation
        pass

class BTree:
    def __init__(self, order):
        self.root = BTreeNode(order)

    def insert(self, key, value):
        self.root.insert(key, value)

    def search(self, key):
        return self.root.search(key)