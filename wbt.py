alpha = 0.1

class Node(object):
    def __init__(self, key, left, right):
        # self.alpha = alpha
        self.key = key
        self.size = 1
        self.size += left.size if left is not None else 0
        self.size += right.size if right is not None else 0
        self.left = left
        self.right = right

    def insert_key(self, key):
        if self.size > 1:
            # check balance
            left = self.left.size if self.left is not None else 0
            right = self.right.size if self.right is not None else 0
            if key >= self.key:
                right += 1
            else:
                left += 1
            if left < alpha*self.size or right < alpha*self.size:
                # need to rebalance
                n = Node.create_tree(self.enumerate(key))
                self.key = n.key
                self.left = n.left
                self.right = n.right
                self.size = n.size
                return

        # actually insert the key
        self.size += 1
        if key >= self.key:
            if self.right is None:
                self.right = Node(key, None, None)
            else:
                self.right.insert_key(key)
        else:
            if self.left is None:
                self.left = Node(key, None, None)
            else:
                self.left.insert_key(key)

    def remove_key(self, key):
        if self.size >= 2:
            # check balance
            left = self.left.size if self.left is not None else 0
            right = self.right.size if self.right is not None else 0
            if key >= self.key:
                right -= 1
            else:
                left -= 1
            if left < alpha*self.size or right < alpha*self.size:
                # need to rebalance
                n = Node.create_tree(self.remove_enumerate(key))
                self.key = n.key
                self.left = n.left
                self.right = n.right
                self.size = n.size
                return

        # actually remove the key
        self.size -= 1
        if key == self.key:
            n = Node.create_tree(self.remove_enumerate(key))
            self.key = n.key
            self.left = n.left
            self.right = n.right
            self.size = n.size
        elif key > self.key:
            if self.right is None:
                print("key does not exist")
                # throw an error
            else:
                self.right.remove_key(key)
        else:
            if self.left is None:
                print("key does not exist")
                # throw an error
            else:
                self.left.remove_key(key)

    def enumerate(self, newKey=None):
        to_return = []
        if self.left is not None:
            if newKey is not None and newKey < self.key:
                to_return = self.left.enumerate(newKey)
            else:
                to_return = self.left.enumerate(None)
        elif newKey is not None and newKey < self.key:
            to_return = [newKey]
        to_return.append(self.key)
        if self.right is not None:
            if newKey is not None and newKey >= self.key:
                to_return.extend(self.right.enumerate(newKey))
            else:
                to_return.extend(self.right.enumerate(None))
        elif newKey is not None and newKey >= self.key:
            to_return.append(newKey)
        return to_return

    def remove_enumerate(self, delKey=None):
        to_return = []
        if self.left is not None:
            if delKey is not None and delKey < self.key:
                to_return = self.left.remove_enumerate(delKey)
            else:
                to_return = self.left.remove_enumerate(None)
        if self.key != delKey:
            to_return.append(self.key)
        if self.right is not None:
            if delKey is not None and delKey > self.key:
                to_return.extend(self.right.remove_enumerate(delKey))
            else:
                to_return.extend(self.right.remove_enumerate(None))
        return to_return

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
        if self.right is not None:
            ret += self.right.tostr(level + 1)
        else:
            ret += "  "*(level+1) + "None\n"
        if self.left is not None:
            ret += self.left.tostr(level + 1)
        else:
            ret += "  "*(level+1) + "None\n"
        return ret

# testing
t = Node.create_tree([1, 5, 10, 11, 12, 13])

print(t)

t.insert_key(2)
print(t)
t.insert_key(2)
print(t)
t.insert_key(2)
print(t)
t.insert_key(2)
print(t)
t.insert_key(2)
print(t)
t.insert_key(2)
print(t)
t.insert_key(2)
print(t)

print("\n\n\n\n\n\n")

t.remove_key(2)
print(t)
t.remove_key(10)
print(t)
t.remove_key(2)
print(t)
t.remove_key(2)
print(t)
t.remove_key(2)
print(t)
t.remove_key(2)
print(t)
t.remove_key(2)
print(t)
t.remove_key(2)
print(t)
t.remove_key(2)
print(t)
# this one fails
t.remove_key(2)
print(t)

print("\n\n\n\n\n")
t.remove_key(11)
print(t)
print("__________")
t.remove_key(1)
print(t)


# print(t)
