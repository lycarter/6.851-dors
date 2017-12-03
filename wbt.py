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

    def rangeQuery(self, xmin, xsup):
        if self.key > xsup: # TODO(lcarter): check equals?
            if self.left is not None:
                return self.left.rangeQuery(xmin, xsup)
            else:
                return []
        elif self.key < xmin:
            if self.right is not None:
                return self.right.rangeQuery(xmin, xsup)
            else:
                return []
        else:
            toReturn = []
            if self.left is not None:
                self.left.searchLeft(xmin, toReturn)
            toReturn.append(self.key)
            if self.right is not None:
                self.right.searchRight(xsup, toReturn)
            return toReturn

    def searchLeft(self, xmin, toReturn):
        if self.left is None and self.right is None:
            if self.key >= xmin:
                toReturn.append(self.key)
        else:
            if self.key >= xmin:
                if self.left is not None:
                    self.left.searchLeft(xmin, toReturn)
                toReturn.append(self.key)
                if self.right is not None:
                    toReturn.extend(self.right.enumerate())
            else:
                self.right.searchLeft(xmin, toReturn)


    def searchRight(self, xmax, toReturn):
        if self.left is None and self.right is None:
            if self.key <= xmax:
                toReturn.append(self.key)
        else:
            if self.key <= xmax:
                if self.left is not None:
                    toReturn.extend(self.left.enumerate())
                toReturn.append(self.key)
                if self.right is not None:
                    self.right.searchRight(xmax, toReturn)
            else:
                self.left.searchRight(xmax, toReturn)


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

class Tester(object):
    def __init__(self):
        pass

    def runAllTests(self):
        print("running tests")
        self.testCreateTree()
        self.testInsert()
        self.testRemove()
        self.testRangeQuery()
        print("all tests succeeded")

    @staticmethod
    def sameSortedList(expected, returned):
        assert(len(expected) == len(returned))
        for i in range(len(expected)):
            assert(expected[i] == returned[i])
        return True

    def testCreateTree(self):
        vals = [1, 5, 10, 11, 12, 13]
        t = Node.create_tree([1, 5, 10, 11, 12, 13])
        assert(Tester.sameSortedList(vals, t.enumerate()))

    def testInsert(self):
        vals = [1, 5, 10, 11, 12, 13]
        t = Node.create_tree([1, 5, 10, 11, 12, 13])
        t.insert_key(2)
        t.insert_key(50)
        assert(Tester.sameSortedList([1, 2, 5, 10, 11, 12, 13, 50], t.enumerate()))

    def testRemove(self):
        vals = [1, 5, 10, 11, 12, 13]
        t = Node.create_tree([1, 5, 10, 11, 12, 13])
        t.insert_key(2)
        t.insert_key(50)
        assert(Tester.sameSortedList([1, 2, 5, 10, 11, 12, 13, 50], t.enumerate()))
        t.remove_key(1)
        t.remove_key(10)
        t.remove_key(50)
        assert(Tester.sameSortedList([2, 5, 11, 12, 13], t.enumerate()))

    def testRangeQuery(self):
        vals = [1, 5, 10, 11, 12, 13]
        t = Node.create_tree([1, 5, 10, 11, 12, 13])
        assert(Tester.sameSortedList([5, 10, 11], t.rangeQuery(5, 11)))
        assert(Tester.sameSortedList([], t.rangeQuery(6, 8)))
        assert(Tester.sameSortedList([1, 5, 10, 11, 12, 13], t.rangeQuery(0, 20)))



t = Tester()
t.runAllTests()

