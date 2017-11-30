class point(object):
	def __init__(self, key, left, right):
		self.key = key
		self.left = left
		self.right = right

class cascaded_array(object):
	def __init__(self, keys)