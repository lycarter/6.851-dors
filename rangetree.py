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
			self.fractions[root.index()] = RangeTree.Fraction(copy.deepcopy(self.points))
			self.buildFractions(root)
		else:
			# invariant: node already has its fraction filled
			index = node.index()
			fro = node.fro
			to = node.to
			if node.lc() is not None:
				self.fractions[node.index()] = RangeTree.Fraction(copy.deepcopy(self.points[node.fro:node.to]))
				RangeTree._linkFraction(self.fractions[index], self.fractions[index].left, self.fractions[node.index()])
				self.buildFractions(node)
			else:
				# Arrays.fill(fractions[index].left, -1)
				self.fractions[index].left = [-1 for i in range(len(self.fractions[index].left))]
			node.become(fro, to)
			if node.rc() is not None:
				self.fractions[node.index()] = RangeTree.Fraction(copy.deepcopy(self.points[node.fro:node.to]))
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
			return RangeTree.Node(fro, to)

	def _splitNode(self, node, start, end):
		if node is None:
			return node
		point = self.get(node)
		if point.x >= end:
			return self._splitNode(node.lc(), start, end)
		elif point.x < start:
			return self._splitNode(node.rc(), start, end)
		else:
			return node

	def _splitPoint(self, start, end):
		node = self._splitNode(start, end)
		return self.get(node) if node is not None else None

	def _getAll(self, out, node, ymin_idx, ysup):
		# print("getting all")
		# print(node)
		# print(ymin_idx)
		# print(ysup)
		if node is None or ymin_idx == -1:
			return
		toAdd = self.fractions[node.index()].points
		# print(toAdd)
		i = ymin_idx
		while i < len(toAdd) and toAdd[i].y < ysup:
			out.append(toAdd[i])
			i += 1

	def _getSmaller(self, out, node, val, ymin_idx, ymin, ysup):
		# print("in get smaller")
		if node is None or ymin_idx == -1:
			return
		frac = self.fractions[node.index()]
		# for point in frac.points:
			# print(point)
		point = self.get(node)
		if point.x < val:
			fro = node.fro
			to = node.to
			if point.y < ysup and point.y >= ymin:
				out.append(point)
			self._getSmaller(out, node.rc(), val, frac.right[ymin_idx], ymin, ysup)
			node.become(fro, to)
			self._getAll(out, node.lc(), frac.left[ymin_idx], ysup)
		else:
			self._getSmaller(out, node.lc(), val, frac.left[ymin_idx], ymin, ysup)

	def _getLargerEqual(self, out, node, val, ymin_idx, ymin, ysup):
		# print("in get larger")
		if node is None or ymin_idx == -1:
			return
		frac = self.fractions[node.index()]
		# for point in frac.points:
			# print(point)
		point = self.get(node)
		# print("point is %s" % point)
		if point.x >= val:
			# print("point is larger than val")
			fro = node.fro
			to = node.to
			if point.y < ysup and point.y >= ymin:
				out.append(point)
			# print("123 node is %s" % node)
			self._getLargerEqual(out, node.lc(), val, frac.left[ymin_idx], ymin, ysup)
			# print("125 node is %s" % node)

			node.become(fro, to)
			# print("128 node is %s" % node)

			self._getAll(out, node.rc(), frac.right[ymin_idx], ysup)
		else:
			self._getLargerEqual(out, node.rc(), val, frac.right[ymin_idx], ymin, ysup)

	def pointsInRange(self, xmin, xsup, ymin, ysup, out=None):
		# print("pointsinrange called")
		if out is None:
			out = []
		node = self._splitNode(self._root(), xmin, xsup)
		if node is None:
			return out

		frac = self.fractions[node.index()]
		# print(frac.points)
		ypoints = frac.points
		# for point in ypoints:
			# print(point)
		ymin_idx = binarySearch(ypoints, Point(float("-inf"), ymin), lambda p: p.y)
		# print "ymin index: %s" % ymin_idx
		if ymin_idx == len(ypoints):
			return []

		point = self.get(node)
		# print(point)
		if point.y < ysup and point.y >= ymin:
			out.append(point)
		# print out


		lc = RangeTree.Node(node.fro, node.to).lc()
		rc = RangeTree.Node(node.fro, node.to).rc()
		self._getSmaller(out, rc, xsup, frac.right[ymin_idx], ymin, ysup)
		# print(out)
		self._getLargerEqual(out, lc, xmin, frac.left[ymin_idx], ymin, ysup)
		# print(out)
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
			print "setting self.fro to " + str(node.fro)
			self.fro = node.fro
			print self.fro
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
			if self.fro is not None and self.to is not None:
				return self.fro + (self.to - self.fro + 1) / 2 - 1
			return 0

		def become(self, fro, to):
			if fro == to:
				return None
			else:
				self.fro = fro
				self.to = to
				return self

		def __str__(self):
			return "(%s,%s):%s" % (self.fro, self.to, self.index())


	def get(self, node):
		return self.points[node.index()]


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

	def __lt__(self, other):
		if self.x != other.x:
			return self.x < other.x
		else:
			return self.y < other.y

	def __le__(self, other):
		if self == other or self < other:
			return True
		return False

	def __gt__(self, other):
		return not self <= other

	def __ge__(self, other):
		return self == other or self > other

	def __hash__(self):
		# print("hey")
		return hash(self.__str__())

	def __str__(self):
		return "(%s,%s)" % (self.x, self.y)


def binarySearch(l, value, comparisonTransform=lambda p: p):
	def _binLowerBound(l, value, lo, hi, ct=lambda p: p):
		if lo > hi:
			return lo

		mid = lo + (hi - lo) / 2
		if (ct(l[mid]) == ct(value)):
			return _binLowerBound(l, value, lo, mid-1, ct)
		elif (ct(l[mid]) > ct(value)):
			return _binLowerBound(l, value, lo, mid-1, ct)
		else:
			return _binLowerBound(l, value, mid+1, hi, ct)

	lo = 0
	hi = len(l) - 1
	return _binLowerBound(l, value, lo, hi, comparisonTransform)




class Tester(object):
	def __init__(self):
		pass

	def runAllTests(self):
		print("running tests")
		self.testXOnlyPointRange()
		self.testPointRange()
		self.makeLargeRangeTree()
		print("all tests passed")

	@staticmethod
	def samePoints(expected, gotten):
		sorted_expected = sorted(expected)
		sorted_gotten = sorted(gotten)
		assert(len(sorted_expected) == len(sorted_gotten))
		for i in range(len(sorted_expected)):
			assert(sorted_gotten[i] == sorted_expected[i])
		return True

	def testXOnlyPointRange(self):
		rt = RangeTree(Point.makeArray([1, 0, 7, 0, 19, 0, 200, 0, 3, 0, 15, 0]))
		points = rt.pointsInRange(6, 20, 0, 1000000)
		assert(Tester.samePoints(Point.makeArray([7,0, 19,0, 15,0]), points))

	def testPointRange(self):
		rt = RangeTree(Point.makeArray([0,0, 5,5, 0,5, 5,0, 2,2, 3,3]))
		points = rt.pointsInRange(-1,6,3,6)
		assert(Tester.samePoints(Point.makeArray([5,5, 3,3, 0,5]), points))

	def makeLargeRangeTree(self):
			rt = RangeTree(Point.makeArray([
			2, 19, 7, 10, 5, 80, 8, 37, 12, 3, 17, 62, 15, 99, 12, 49, 41, 95, 58, 59, 93, 70, 33,
			30, 52, 23, 67, 89]))




Tester().runAllTests()