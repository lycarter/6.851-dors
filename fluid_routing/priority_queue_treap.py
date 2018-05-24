"""Implements a priority queue for LPA*"""

import treap


class Queue():
    """Shim for treap to make it look like Queue.

    Note: This can be copy.deepcopy'd correctly."""
    def __init__(self):
        self._treap = treap.Treap()
        self._set = set([])

    def insert(self, item):
        self._treap.insert(item)
        self._set.add(item)

    def top(self):
        if self._treap.find_kth(1) is None:
            return None
        else:
            return self._treap.find_kth(1).key

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
        print("pop called")
        item = self._treap.find_kth(1).key
        print("item is %s" % (item,))
        if self._treap.find(item):
            print("\ttreap has item")
        else:
            print("\t\t\t\ttreap does not have item")
            print(self._treap.find_kth(1).key)
            print(self._treap.size())
        self._set.remove(item)
        print("\tresult of treap delete: %s" % (self._treap.delete(item),))
        if self._treap.find(item):
            print("\t\t\t\ttreap *still* has item")
            print(self._treap)
        else:
            print("\ttreap has removed item")

        return item

    def remove(self, item):
        self._set.remove(item)
        self._treap.delete(item)

    def __contains__(self, key):
        return key in self._set

    def __len__(self):
        return self._treap.size()

    def printQueue(self):
        print(self._treap)