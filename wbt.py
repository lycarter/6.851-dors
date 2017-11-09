class Node(Object):
	def __init__(self, key, left, right):
		self.key = key
		self.size = 1
		self.size += left.size if left is not None else 0
		self.size += right.size if right is not None else 0
		self.left = left
		self.right = right

	def insert_key(self, key, to_check=None):
		to_check.append(self)
		self.size += 1
		if key >= self.key:
			if self.right is None:
				self.right = Node(key, None, None)
				Node.check_balance(to_check)
			else:
				self.right.insert_key(key, to_check)
		else:
			if self.left is None:
				self.left = Node(key, None, None)
				Node.check_balance(to_check)
			else:
				self.left.insert_key(key, to_check)

	def enumerate(self):
		to_return = []
		if self.left is not None:
			to_return = self.left.enumerate
		to_return.append(self.key)
		if self.right is not None:
			to_return.extend(self.right.enumerate)
		return to_return

	@classmethod
	def check_balance(to_check):
		# checks whether any of the nodes in to_check are unbalanced, and rebalances the entire subtree if so


	# rebalance this tree by creating a perfectly balanced tree for this subtree,
	# including new node key
	def rebalance(self, key):

	def __str__(self):
		return str(self.size)

class WBT(Object):
	def __init__(self):
