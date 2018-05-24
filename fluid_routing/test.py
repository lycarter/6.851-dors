import sortedcontainers
import random

class dummy():
    def __init__(self, val):
        self.val = val
        self.otherval = random.random

    def __hash__(self):
        return hash(self.val)

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return not self == other

    def _kCompare(self, other):
        if isinstance(other, self.__class__):
            # Lexicographic sorting
            return other.val - self.val
        else:
            return NotImplemented

    def __lt__(self, other):
        return self._kCompare(other) > 0

    def __gt__(self, other):
        return self._kCompare(other) < 0

    def __le__(self, other):
        return self._kCompare(other) >= 0

    def __ge__(self, other):
        return self._kCompare(other) <= 0

    def __str__(self):
        return "val: %s, rand: %s" % (self.val, self.otherval)


a = sortedcontainers.SortedSet()

a.add(dummy(1))
a.add(dummy(1))
a.remove(dummy(1))
print(len(a))