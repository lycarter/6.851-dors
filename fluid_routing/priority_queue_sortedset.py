"""Implements a priority queue for LPA*"""

import sortedcontainers
import copy

class queue():
    """Shim for treap to make it look like Queue.

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

    # def remove(self, item):
    #     print("called from elsewhere")
    #     self._treap.remove(item)

    def remove(self, item):
        self._set.discard(item)
        try:
            self._set.discard(item)
        except Exception, e:
            print item
            print("discarding???")
            print item in self._set
            print "\n".join([str(i) for i in self._set])
            raise e

    def __contains__(self, key):
        return key in self._set

    def __len__(self):
        return len(self._set)

    def printQueue(self):
        print(self._set)


    def __deepcopy__(self, memo):
        result = queue()
        memo[id(self)] = result
        tmpItem = self.top()
        # if isinstance(tmpItem, NodeState):
        #     new_state_factory = copy.deepcopy(tmpItem.state_factory, memo)
        #     new_node_lookup_dict = copy.deepcopy(tmpItem.new_node_lookup_dict, memo)
        #     for item in self._set:
        #         newItem = copy.copy(item)
        #         newItem.set_node_lookup_dict(new_node_lookup_dict)
        #         newItem.set_state_factory(new_state_factory)
        #         result.insert(newItem)
        # else:
        for item in self._set:
            result.insert(copy.deepcopy(item, memo))
        return result