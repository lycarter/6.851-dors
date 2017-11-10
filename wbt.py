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
            # print("branch 1")
            left = self.left.size if self.left is not None else 0
            right = self.right.size if self.right is not None else 0
            if key >= self.key:
                right += 1
            else:
                left += 1
            # print("left: %s, right: %s" % (left, right))
            if left < alpha*self.size or right < alpha*self.size:
                print("rebalancing")
                # print("enumerated: %s" % (', '.join(self.enumerate(key))))
                n = Node.create_tree(self.enumerate(key))
                self.key = n.key
                self.left = n.left
                self.right = n.right
                self.size = n.size
                return

        self.size += 1
        # print("inserting %s" % key)
        if key >= self.key:
            if self.right is None:
                self.right = Node(key, None, None)
            else:
                self.right.insert_key(key)
        else:
            # print("41")
            if self.left is None:
                # print("43")
                self.left = Node(key, None, None)
            else:
                # print("46")
                self.left.insert_key(key)

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

    # @staticmethod
    # def check_balance(to_check):
    #     # checks whether any of the nodes in to_check are unbalanced, and rebalances the entire subtree if so
    #     # for node in to_check:
    #     #     print node
    #     for i in range(len(to_check)):
    #         node = to_check[i]
    #         left = node.left.size if node.left is not None else 0
    #         right = node.right.size if node.right is not None else 0
    #         if left < alpha*node.size or right < alpha*node.size:
    #             print("rebalancing")
    #             print("input: %s", (node.enumerate(),))
    #             to_check[i] = Node.create_tree(node.enumerate())
    #             print("output:")
    #             print(node)
    #             break

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

# print(t)
