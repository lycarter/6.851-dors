"""LPA* implementation in Python."""

import priority_queue as pq

# c: cost
# g*(s): dist from start to s
# h(s, s_goal): heuristic (nonnegative, obey triangle ineq)
# g(s): estimate of g*(s)
# rhs(s): 0 if s is start, min route to s from pred(s) otherwise

# k1 = min(g(s), rhs(s) + h(s, sgoal)) (travel cost to start + heuristic to goal)
# k2 = min(g(s), rhs(s))               (travel cost to start approx)

# overconsistent: g(s) > rhs(s)  --> set g(s) = rhs(s)
# underconsistent: g(s) < rhs(s) --> set g(s) = inf

class state():
    """An arbitrary-dimension state for LPA*"""

    def __init__(self, pos, k):
        """Sets position and k variables"""
        self.pos = pos
        self.k = k
        assert isinstance(self.k, tuple)
        assert len(self.k) == 2
        assert isinstance(self.pos, tuple)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.pos == self.pos
        return NotImplemented

    def __ne__(self, other):
        res = self.__eq__(other)
        if res is NotImplemented:
            return res
        else:
            return not res

    def __hash__(self):
        return hash(self.pos)

    def _kCompare(self, other):
        if isinstance(other, self.__class__):
            # Lexicographic sorting
            if other.k[0] == float("inf") and self.k[0] == float("inf"):
                first = 0
            else:
                first = other.k[0] - self.k[0]

            if other.k[1] == float("inf") and self.k[1] == float("inf"):
                second = 0
            else:
                second = other.k[1] - self.k[1]

            if first != 0:
                return first
            else:
                return second
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

    def pred(self):
        """Possible parents of this node.

        This should be overridden by child classes."""
        pass

    def succ(self):
        """Possible children of this node.

        This should be overridden by child classes."""
        pass

    def __str__(self):
        return "pos: %s, k: %s" % (self.pos, self.k)


class LPA():
    def __init__(self, sStart, sGoal, stateDict, debug=False):
        """Initializes LPA* class.

        Args:
            sStart: Starting state (type: state)
            sGoal: Ending state (type: state)
            stateDict: A dictionary to find the most current version of a state.
        """

        # U is a priority queue of inconsistent nodes (g != rhs)
        self._U = pq.queue()

        # Warning that for these two dicts, the keys compare by position,
        # but the key isn't updated with the latest k value
        # This shouldn't cause any problems in any reasonable use.

        # Basically, just don't ever use the keys for anything except insert/retrieve

        self._g_dict = {}
        self._rhs_dict = {}

        self._impassable_nodes = set([])
        self._impassable_edges = set([])

        self.sGoal = sGoal
        self.sStart = sStart
        self.debug = debug
        self.state_factory = sStart.state_factory

        self._rhs_dict[sStart] = 0

        sStart.k = self._calculateKey(sStart)
        self._U.insert(sStart)

        self.stateDict = stateDict
        self.stateDict[sStart] = sStart

    def _g(self, s):
        return self._g_dict.get(s, float("inf"))

    def _rhs(self, s):
        if s == self.sStart:
            return 0
        else:
            return self._rhs_dict.get(s, float("inf"))

    def _printGRHS(self):
        print "The state of g, rhs:"
        candidates = set(self._g_dict.keys())
        candidates.update(set(self._rhs_dict.keys()))
        for k in candidates:
            print "%s: (%s, %s)" % (k.pos, self._g(k), self._rhs(k))

    def _printQueue(self):
        print "the state of the queue:"
        self._U.printQueue()

    def _printRHS(self):
        print "The state of rhs:"
        for k, v in self._rhs_dict.iteritems():
            print "%s: %s" % (k.pos, self._rhs(k))


    def _calculateKey(self, s):
        """Updates the key for a specific ndoe."""
        return (min(self._g(s), self._rhs(s)) + self._h(s, self.sGoal),
                min(self._g(s), self._rhs(s)))

    def _h(self, s, sGoal):
        """Heuristic obeying the triangle inequality. This should be overridden in derivative classes."""
        pass

    def _c(self, s, s2):
        """Cost to move from s to s2. This should be overridden in derivative classes."""
        pass

    def _updateVertex(self, u):
        if u != self.sStart:
            # Update the estimate with lowest cost from predecessors
            self._rhs_dict[u] = min([self._g(s) + self._c(s, u) for s in u.pred()])
        if u in self._U:
            self._U.remove(u)
        if self._g(u) != self._rhs(u):
            u.k = self._calculateKey(u)
            self._U.insert(u)
            self.stateDict[u] = u

    def computeShortestPath(self):
        while (self._U.topKey() < self._calculateKey(self.sGoal) or
               self._rhs(self.sGoal) != self._g(self.sGoal)):
            if self.debug: self._printQueue()
            u = self._U.pop()
            if self.debug: print "now looking at %s" % (u.pos,)
            if self.debug: self._printGRHS()
            if self._g(u) > self._rhs(u):
                self._g_dict[u] = self._rhs(u)
                for s in u.succ():
                    if self.debug: print "updating %s" % (s.pos,)
                    self._updateVertex(s)
                    if self.debug: self._printGRHS()
            else:
                self._g_dict[u] = float("inf")
                # self._updateVertex(u)
                for s in u.succ():
                    self._updateVertex(s)

    def getShortestPath(self):
        # Make sure to only run this after computeShortestPath
        if self.debug: print "\tgeting shortest path"
        sCur = self.sGoal
        path = [sCur]
        totalCost = 0

        while sCur != self.sStart:
            if self.debug: print "\tfinding new node to add"
            minCost = float("inf")
            sNext = None
            for sPred in sCur.pred():
                tmpCost = self._g(sPred) + self._c(sPred, sCur)
                if self.debug: print("\tgot a min cost of %s with a tmp cost of %s"
                    % (minCost, tmpCost))
                minCost = min(minCost, tmpCost)
                if tmpCost == minCost and tmpCost != float("inf"):
                    moveCost = self._c(sPred, sCur)
                    sNext = sPred

            if sNext is None:
                return (None, float("inf"))
            sCur = sNext
            path.append(sCur)
            totalCost += moveCost

        if self.debug: print totalCost
        return (path[::-1], totalCost)

    def make_node_impassable(self, pos):
        """This should be overridden in derivative classes."""
        pass

    def make_edge_impassable(self, edge):
        """This should be overridden in derivative classes."""
        pass

    # def __eq__(self, other):
    #     if isinstance(self, other.__class__):
    #         return self._impassable_edges == other._impassable_edges && self._impassable_nodes == other._impassable_nodes
    #     else:
    #         return NotImplemented
    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # def __hash__(self):
    #     return hash((tuple(self._impassable_nodes), tuple(self._impassable_edges)))