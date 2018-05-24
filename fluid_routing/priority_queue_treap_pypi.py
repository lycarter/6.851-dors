"""Implements a priority queue for LPA*"""

import treap


class queue():
    """Shim for treap to make it look like Queue.

    Note: This can be copy.deepcopy'd correctly."""
    def __init__(self):
        self._treap = treap.treap()
        self._counter = 0
        self.time_lookup = {}

    def insert(self, item):
        self.time_lookup[item] = self._counter
        self._counter += 1
        self._treap[item] = 1

    def top(self):
        try:
            return self._treap.find_min()
        except KeyError:
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
        try:
            item = self._treap.find_min()
            self._treap.remove_min()
        except KeyError:
            item = None
        return item

    def remove(self, item):
        del self._treap[item]

    def __contains__(self, key):
        return key in self._treap

    def __len__(self):
        return len(self._treap)

    def printQueue(self):
        print(self._treap)

    def __str__(self):
        toReturn = "note: this destroys the queue\n\n"
        while len(self._treap) > 0:
            u = self.pop()
            toReturn += "(%s) %s\n" % (self.time_lookup[u], str(u))
        return toReturn