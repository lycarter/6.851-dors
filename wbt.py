alpha = 0.1

class dummyDs(object):
    def __init__(self):
        pass

    def insert_key(self, key):
        pass

    def remove_key(self, key):
        pass

    def factory(self, arg):
        return dummyDs()

class Node(object):
    def __init__(self, key, left, right, next_dim_ds=None):
        # self.alpha = alpha
        self.key = key
        self.size = 1
        self.size += left.size if left is not None else 0
        self.size += right.size if right is not None else 0
        self.left = left
        self.right = right
        if next_dim_ds is None:
            next_dim_ds = dummyDs()
        self.next_dim_ds = next_dim_ds

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
                self.next_dim_ds = n.next_dim_ds
                return

        # actually insert the key
        self.size += 1
        self.next_dim_ds.insert_key(key)
        if key >= self.key:
            if self.right is None:
                self.right = Node(key, None, None, self.next_dim_ds.factory([key]))
            else:
                self.right.insert_key(key)
        else:
            if self.left is None:
                self.left = Node(key, None, None, self.next_dim_ds.factory([key]))
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
                self.next_dim_ds = n.next_dim_ds
                return

        # actually remove the key
        self.size -= 1
        self.next_dim_ds.remove_key(key)
        if key == self.key:
            n = Node.create_tree(self.remove_enumerate(key))
            self.key = n.key
            self.left = n.left
            self.right = n.right
            self.size = n.size
            self.next_dim_ds = n.next_dim_ds
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

    def rangeQuery(self, rawMin, rawMax, toReturn=None):
        minCoords = [min(rawMin.coords[i], rawMax.coords[i]) for i in range(len(rawMin.coords))]
        pointMin = Point(minCoords)
        maxCoords = [max(rawMin.coords[i], rawMax.coords[i]) for i in range(len(rawMin.coords))]
        pointMax = Point(maxCoords)
        if self.key > pointMax:
            if self.left is not None:
                return self.left.rangeQuery(pointMin, pointMax)
            else:
                return []
        elif self.key < pointMin:
            if self.right is not None:
                return self.right.rangeQuery(pointMin, pointMax)
            else:
                return []
        else:
            toReturn = []
            if self.left is not None:
                self.left.searchLeft(pointMin, pointMax, toReturn)

            if self.key >= pointMin and self.key <= pointMax:
                toReturn.append(self.key)

            if self.right is not None:
                self.right.searchRight(pointMin, pointMax, toReturn)
            return toReturn

    def searchLeft(self, pointMin, pointMax, toReturn):
        if self.left is None and self.right is None:
            if self.key <= pointMax and self.key >= pointMin:
                toReturn.append(self.key)
        else:
            if self.key >= pointMin:
                if self.left is not None:
                    self.left.searchLeft(pointMin, pointMax, toReturn)

                if self.key >= pointMin and self.key <= pointMax:
                    toReturn.append(self.key)

                if self.right is not None:
                    if len(self.key.coords) == 1:
                        toReturn.extend(self.right.enumerate())
                    else:
                        toReturn.extend(self.right.next_dim_ds.rangeQuery(pointMin, pointMax, toReturn))
            else:
                self.right.searchLeft(pointMin, pointMax, toReturn)


    def searchRight(self, pointMin, pointMax, toReturn):
        if self.left is None and self.right is None:
            if self.key >= pointMin and self.key <= pointMax:
                toReturn.append(self.key)
        else:
            if self.key <= pointMax:
                if self.left is not None:
                    if len(self.key.coords) == 1:
                        toReturn.extend(self.left.enumerate())
                    else:
                        toReturn.extend(self.left.next_dim_ds.rangeQuery(pointMin, pointMax, toReturn))
                
                if self.key <= pointMax and self.key >= pointMin:
                    toReturn.append(self.key)

                if self.right is not None:
                    self.right.searchRight(pointMin, pointMax, toReturn)
            else:
                self.left.searchRight(pointMin, pointMax, toReturn)


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
    def create_tree(points):
        if len(points) == 1:
            return Node(points[0], None, None)
        elif len(points) == 2:
            left = Node(points[0], None, None)
            return Node(points[1], left, None)
        else:
            left = Node.create_tree(points[0:len(points)/2])
            right = Node.create_tree(points[len(points)/2 + 1:])
            return Node(points[len(points)/2], left, right)

    def factory(self, points):
        return Node.create_tree(points)

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

class Point(object):
    def __init__(self, coords):
        self.coords = coords

    def __eq__(self, other):
        if other is None:
            return False
        return self.coords == other.coords

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.coords[0] == other.coords[0]:
            return self.child() < other.child()
        return self.coords[0] < other.coords[0]

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return self == other or self > other

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        s = [str(c) for c in self.coords]
        return '(' + ','.join(s) + ')'

    def child(self):
        if len(self.coords) > 1:
            return Point(self.coords[1:])
        else:
            return None

class Tester(object):
    def __init__(self):
        pass

    def runAllTests(self):
        self.points = [Point([key]) for key in [1, 5, 10, 11, 12, 13]]
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
        t = Node.create_tree(self.points)
        assert(Tester.sameSortedList(self.points, t.enumerate()))

    def testInsert(self):
        t = Node.create_tree(self.points)
        t.insert_key(Point([2]))
        t.insert_key(Point([50]))
        assert(Tester.sameSortedList([Point([key]) for key in [1, 2, 5, 10, 11, 12, 13, 50]], t.enumerate()))

    def testRemove(self):
        t = Node.create_tree(self.points)
        t.insert_key(Point([2]))
        t.insert_key(Point([50]))
        assert(Tester.sameSortedList([Point([key]) for key in [1, 2, 5, 10, 11, 12, 13, 50]], t.enumerate()))
        t.remove_key(Point([1]))
        t.remove_key(Point([10]))
        t.remove_key(Point([50]))
        assert(Tester.sameSortedList([Point([key]) for key in [2, 5, 11, 12, 13]], t.enumerate()))

    def testRangeQuery(self):
        t = Node.create_tree(self.points)
        assert(Tester.sameSortedList([Point([key]) for key in [5, 10, 11]], t.rangeQuery(Point([5]), Point([11]))))
        assert(Tester.sameSortedList([], t.rangeQuery(Point([6]), Point([8]))))
        assert(Tester.sameSortedList(self.points, t.rangeQuery(Point([0]), Point([20]))))



t = Tester()
t.runAllTests()

