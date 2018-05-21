import priority_queue as pq1
import priority_queue_dict as pq2
import random

class DummyItem():
	def __init__(self, k):
		self.k = k

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return other.k == self.k
		return NotImplemented

	def __ne__(self, other):
		res = self.__eq__(other)
		if res is NotImplemented:
			return res
		else:
			return not res

	def __hash__(self):
		return hash(self.k)

	def _kCompare(self, other):
		if isinstance(other, self.__class__):
			# Lexicographic sorting
			return other.k - self.k
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


def generate_item():
	return DummyItem(random.random())

pqInst1 = pq1.queue()
pqInst2 = pq2.queue()

items = set([])

for i in range(10):
	print("starting trial %s" % i)
# test insert
	for i in range(20):
		item = generate_item()
		items.add(item)
		pqInst1.insert(item)
		pqInst2.insert(item)

	# test top & pop
	for i in range(10):
		assert(pqInst1.top() == pqInst2.top())
		itemPopped = pqInst1.pop()
		assert(itemPopped == pqInst2.pop())
		items.remove(itemPopped)

	for i in range(10):
		itemToRemove = items.pop()
		pqInst1.remove(itemToRemove)
		pqInst2.remove(itemToRemove)
		assert(pqInst1.topKey() == pqInst2.topKey())


