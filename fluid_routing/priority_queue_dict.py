"""Implements a priority queue for LPA*"""


class Queue():
    """Linked list augmented with hashtable.

    Note: This can be copy.deepcopy'd correctly."""
    def __init__(self):
        self._U = {}
        self._list_U = None

    def insert(self, item):
        listItem = LinkedList(item)
        if self._list_U == None:
            self._list_U = listItem
        else:
            self._list_U.add(listItem)
            if self._list_U.prev:
                self._list_U = self._list_U.prev
        self._U[item] = listItem

    def top(self):
        if self._list_U:
            return self._list_U.val
        else:
            return None

    def topKey(self):
        t = self.top()
        if type(t) == tuple:
            return t
        else:
            if t is None:
                return (float("inf"), float("inf"))
            else:
                return t.k

    def pop(self):
        topListItem = self._list_U
        self._list_U = topListItem.next
        item = topListItem.pop()
        del self._U[item]
        return item

    def remove(self, item):
        listItem = self._U[item]
        if listItem == self._list_U:
            self._list_U = self._list_U.next
        listItem.pop()
        del self._U[item]


    def __contains__(self, key):
        return key in self._U

    def __len__(self):
        return len(self._U)

    def printQueue(self):
        for u in self._U:
            print u

class LinkedList():
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

    def pop(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev
        return self.val

    def add(self, other):
        if self.val > other.val:
            other.prev = self.prev
            other.next = self
            if self.prev:
                self.prev.next = other
            self.prev = other
        else:
            if self.next:
                self.next.add(other)
            else:
                other.prev = self
                self.next = other

    def __str__(self):
        if self.prev and self.next:
            selfStr = "(%s <- %s -> %s)" % (self.prev.val.k, self.val.k, self.next.val.k)
        elif self.prev:
            selfStr = "(%s <- %s -X)" % (self.prev.val.k, self.val.k)
        elif self.next:
            selfStr = "(X- %s -> %s)" % (self.val.k, self.next.val.k)
        else:
            selfStr = "(X- %s -X)" % (self.val.k,)
        return selfStr + ", " + str(self.next)