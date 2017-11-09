class Node(object):
    def __init__(self, key, left, right):
        self.key = key
        self.size = 1
        self.size += left.size if left is not None else 0
        self.size += right.size if right is not None else 0
        self.left = left
        self.right = right

    def insert_key(self, key, to_check=None):
        if self.size > 1:
            to_check.append(self)
        self.size += 1
        if key >= self.key:
            if self.right is None:
                self.right = Node(key, None, None)
                Node.check_balance(to_check)
            else:
                self.right.insert_key(key, to_check)
        else:
            if self.left is None:
                self.left = Node(key, None, None)
                Node.check_balance(to_check)
            else:
                self.left.insert_key(key, to_check)

    def enumerate(self):
        to_return = []
        if self.left is not None:
            to_return = self.left.enumerate
        to_return.append(self.key)
        if self.right is not None:
            to_return.extend(self.right.enumerate)
        return to_return

    @staticmethod
    def check_balance(to_check):
        # checks whether any of the nodes in to_check are unbalanced, and rebalances the entire subtree if so
        for node in to_check:
            if node.left.size < alpha*node.size or node.right.size < alpha*node.size:
                node = create_tree(node.enumerate())
                break

    @staticmethod
    def create_tree(keys):
        if len(keys) == 1:
            return Node(keys[0], None, None)
        elif len(keys) == 2:
            left = Node(keys[0], None, None)
            return Node(keys[1], left, None)
        else:
            left = Node.create_tree(keys[0:len(keys)/2])
            right = Node.create_tree(keys[len(keys)/2 + 1:])
            return Node(keys[len(keys)/2], left, right)

    def __str__(self):
        return self.tostr()

    def tostr(self, level=0):
        ret = "  "*level + str(self.key) + "\n"
        if self.left is None and self.right is None:
            return ret
        if self.left is not None:
            ret += self.left.tostr(level + 1)
        else:
            ret += "  "*(level+1) + "None\n"
        if self.right is not None:
            ret += self.right.tostr(level + 1)
        else:
            ret += "  "*(level+1) + "None\n"
        return ret

# testing
t = Node.create_tree([1, 5, 10, 11, 12, 13])

print(t)
