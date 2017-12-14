"""Implements a priority queue for LPA*"""

import heapq


class queue():
    """Shim for heapq to make it look like Queue.

    Note: This can be copy.deepcopy'd correctly."""
    def __init__(self):
        self._U = []
        self._set = set([])

    def insert(self, item):
        heapq.heappush(self._U, item)
        self._set.add(item)

    def top(self):
        if len(self._U) > 0:
            return self._U[0]
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
        item = heapq.heappop(self._U)
        self._set.remove(item)
        return item

    def remove(self, item):
        # Note that this is a linear-time operation. Reimplementing as a treap would
        # reduce this to logarithmic time without any further penalties.
        self._set.remove(item)
        self._U.remove(item)
        heapq.heapify(self._U)


    def __contains__(self, key):
        return key in self._set

    def __len__(self):
        return len(self._U)

    def printQueue(self):
        for u in self._U:
            print u