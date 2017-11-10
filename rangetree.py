import copy

# translation of https://github.com/elazarl/RangeTree/blob/master/src/main/java/com/github/elazarl/rangetree/RangeTree.java

class RangeTree(object):
	def __init__(self, points):
		self.points = points
		points.sort(key=lambda p: p.x)
		self.fractions = [None]*len(points)
		self.buildFractions()

	def buildFractions(self, node=None):
		if node is None:
			root = self._root()
			self.fractions[root.index()] = Fraction(copy.deepcopy(self.points))
			self.buildFractions(root)
		else:
			# invariant: node already has its fraction filled
			index = node.index()
			fro = node.fro
			to = node.to
			if node.lc() is not None:
				self.fractions[node.index()] = Fraction(copy.deepcopy(self.points[node.fro:node.to]))
				RangeTree._linkFraction(self.fractions[index], self.fractions[index].left, self.fractions[node.index()])
				self.buildFractions(node)
			else:
				# Arrays.fill(fractions[index].left, -1)
				self.fractions[index].left = [-1 for i in range(len(self.fractions[index].left))]
			node.become(fro, to)
			if node.rc() is not None:
				self.fractions[node.index()] = Fraction(copy.deepcopy(self.points[node.fro:node.to]))
				RangeTree._linkFraction(self.fractions[index], self.fractions[index].right, self.fractions[node.index()])
				self.buildFractions(node)
			else:
				self.fractions[index].right = [-1 for i in range(len(self.fractions[index].right))]

	@staticmethod
	def _linkFraction(parent, parentLinks, child):
		p = 0
		c = 0
		while (p < len(parentLinks) and c < len(child.points)):
			if child.points[c].y >= parent.points[p].y:
				parentLinks[p] = c
				p += 1
			else:
				c += 1
		for i in range(p, len(parentLinks)):
			parentLinks[i] = -1

	def _root(self):
		return RangeTree._make(0, len(self.points))

	@staticmethod
	def _make(fro, to):
		if fro == to:
			return None
		else:
			return Node(fro, to)

	@staticmethod
	def _splitNode(node, start, end):
		if node is None:
			return node
		point = node.get()
		if point.x >= end:
			return _splitNode(node.lc(), start, end)
		elif point.x < start:
			return _splitNode(node.rc(), start, end)
		else:
			return node

	@staticmethod
	def _splitPoint(self, start, end):
		node = _splitNode(start, end)
		return node.get() if node is not None else None

	def _getAll(self, out, node, ymin_ix, ysup):
		if node is None or ymin_ix == -1:
			return
		toAdd = self.fractions[node.index()].points
		i = ymin_ix
		while i < len(toAdd) and toAdd[i].y < ysup:
			out.append(toAdd[i])

	def _getSmaller(self, out, node, val, ymin_ix, ymin, ysup):
		if node is None or ymin_ix == -1:
			return
		frac = self.fractions[node.index()]
		point = node.get()
		if point.x < val:
			fro = node.fro
			to = node.to
			if point.y < ysup and point.y >= ymin:
				out.append(point)
			self._getSmaller(out, node.rc(), val, frac.right[ymin_ix], ymin, ysup)
			node.become(fro, to)
			self._getAll(out, node.lc(), frac.left[ymin_ix], ysup)
		else:
			self.getSmaller(out, node.lc(), frac.left[ymin_ix], ymin, ysup)

	def _getLargerEqual(self, out, node, val, ymin_ix, ymin, ysup):
		if node is None or ymin_ix == -1:
			return
		frac = self.fractions[node.index()]
		point = node.get()
		if point.x >= val:
			fro = node.fro
			to = node.to
			if point.y < ysup and point.y >= ymin:
				out.append(point)
			self._getLargerEqual(out, node.lc(), val, frac.left[ymin_ix], ymin, ysup)
			node.become(fro, to)
			self._getAll(out, node.rc(), frac.left[ymin_ix], ysup)
		else:
			self._getLargerEqual(out, node.rc(), frac.right[ymin_ix], ymin, ysup)

	def pointsInRange(self, xmin, xsup, ymin, ysup, out=[]):
		node = RangeTree._splitNode(self._root(), xmin, xsup)
		if node is None:
			return
		frac = self.fractions[node.index()]
		ypoints = self.fractions[node.index()].points
		# todo:
		#         int ymin_ix = Arrays.binarySearch(ypoints, Point.make(Double.NEGATIVE_INFINITY, ymin), compareYCoord)
		if ymin_ix < 0:
			ymin_ix = -1*ymin_ix - 1
		if ymin_ix == len(ypoints):
			return
		point = node.get()
		if point.y < ysup and point.y >= ymin:
			out.append(point)
		lc = Node().fromNode(node).lc()
		rc = Node().fromNode(node).rc()
		self._getSmaller(rc, xsup, frac.right[ymin_ix], ymin, ysup, out)
		self._getLargerEqual(lc, xmin, frac.left[ymin_ix], ymin, ysup, out)
		return out

	def path(self, dirs):
		# for debugging only
		node = self._root()
		result = []
		result.append(self.points[node.index()])
		for d in dirs:
			if node is None:
				continue
			if d == 'l':
				node = node.lc()
			else:
				node = node.rc()
			result.append(points[node.index()] if node is not None else None)
		return result

class Fraction(object):
	def __init__(self, points):
		self.points = points
		self.points.sort(key=lambda i: i.y)
		self.right = [None]*len(points)
		self.left = [None]*len(points)

class Node(object):
	def __init__(self, fro=None, to=None):
		self.fro = fro
		self.to = to

	def fromNode(self, node):
		self.fro = node.fro
		self.to = node.to

	def rc(self):
		if self.to - self.fro == 1:
			return None
		else:
			return self.become(self.index() + 1, self.to)

	def lc(self):
		if self.to - self.fro == 1:
			return None
		else:
			return self.become(self.fro, self.index())

	def index(self):
		return self.fro + (self.to - self.fro + 1) / 2 - 1

	def get(self):
		return self.points[self.index()]

	def become(self, fro, to):
		if fro == to:
			return None
		else:
			self.fro = fro
			self.to = to
			return self

	def __str__(self):
		return "[" + self.fro + "," + self.to + ")[" + self.index() + "]=" + self.get()


class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	@staticmethod
	def makeArray(points):
		if len(points) % 2 != 0:
			# throw new error
			return
		result = []
		for i in range(0, len(points), 2):
			result.append(Point(points[i], points[i+1]))
		return result

	def __eq__(self, other):
		if other.x == self.x and other.y == self.y:
			return True
		return False

	def __ne__(self, other):
		return not self == other

	def __str__(self):
		return "(" + x + "," + y + ")"



class Tester(object):
	def __init__(self):
		pass

	def runAllTests(self):
		self.testXOnlyPointRange()

	def testXOnlyPointRange(self):
		rt = RangeTree(Point.makeArray([1, 0, 7, 0, 19, 0, 200, 0, 3, 0, 15, 0]))
		assert(set(rt.pointsInRange(6, 20, 0, 10000000)) == set(Point.makeArray([7, 0, 19, 0, 15, 0])))
		assert(set(rt.pointsInRange(1, 10, 0, 10000000)) == set(Point.makeArray([7, 0, 1, 0, 3, 0])))
		rt = RangeTree(Point.makeArray([
			2, 19, 7, 10, 5, 80, 8, 37, 12, 3, 17, 62, 15, 99, 12, 49, 41, 95, 58, 59, 93, 70, 33,
			30, 52, 23, 67, 89]))
		print("yay success")
		print(rt)

	def testPointRange(self):
		pass




Tester().runAllTests()