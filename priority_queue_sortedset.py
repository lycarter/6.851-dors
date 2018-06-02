"""Implements a priority queue for LPA*"""

import sortedcontainers
import copy

class Queue():
    """Treap augmented with hashtable.

    Note: This can be copy.deepcopy'd correctly."""
    def __init__(self):
        self._set = sortedcontainers.SortedSet()

    def insert(self, item):
        self._set.add(item)

    def top(self):
        try:
            return self._set[0]
        except IndexError:
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
            item = self._set.pop(0)
        except IndexError:
            item = None
        return item

    def remove(self, item):
        self._set.remove(item)

    def __contains__(self, key):
        return key in self._set

    def __len__(self):
        return len(self._set)

    def printQueue(self):
        print(self._set)


    def __deepcopy__(self, memo):
        result = Queue()
        memo[id(self)] = result
        tmpItem = self.top()
        for item in self._set:
            result.insert(copy.deepcopy(item, memo))
        return result