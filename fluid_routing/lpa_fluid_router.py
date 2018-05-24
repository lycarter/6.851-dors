"""Simultaneous fluid channel routing in 3D-space."""

import lpa_star
import copy

#pylint: disable=attribute-defined-outside-init


class NodeState(lpa_star.state):
    """State subclass which defines nodes for fluid routing."""
    def set_node_lookup_dict(self, node_lookup_dict):
        self.lookup_dict = node_lookup_dict

    def set_valid_pos_lookup_func(self, pos_f):
        self.is_valid_pos_f = pos_f

    def set_state_factory(self, state_factory):
        self.state_factory = state_factory

    def pred(self):
        preds = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if (i, j, k) == (0, 0, 0):
                        continue
                    possible_pos = (self.pos[0] + i, self.pos[1] + j, self.pos[2] + k)
                    state = self.state_factory.make_or_get_state_by_pos(possible_pos)
                    if state is not None:
                        preds.append(state)
        return preds

    def succ(self):
        return self.pred()

    def __deepcopy__(self, memo):
        result = NodeState(self.pos[:], self.k[:])
        memo[id(self)] = result
        result.set_node_lookup_dict(copy.deepcopy(self.lookup_dict, memo))

        # This does not have to be deepcopy'd, because the same region is
        # still valid for all copied objects. Only the cost function is updated
        # when setting a node as inadmissable
        result.set_valid_pos_lookup_func(self.is_valid_pos_f)

        result.set_state_factory(copy.deepcopy(self.state_factory, memo))
        return result


class FluidLPA(lpa_star.LPA):
    """LPA* subclass which defines the heuristic and cost functions for fluid
    LPA*.
    """
    def _h(self, s, s_goal):
        return self._c(s, s_goal)

    def _c(self, s, s2):
        if s.pos in self._impassable_nodes or s2.pos in self._impassable_nodes:
            return float("inf")
        if (s, s2) in self._impassable_edges or (s2, s) in self._impassable_edges:
            return float("inf")
        p_1 = s.pos
        p_2 = s2.pos
        return sum([(p_1[i] - p_2[i])**2 for i in range(3)])**0.5

    def make_node_impassable(self, impassable_node):
        self._impassable_nodes.add(impassable_node.pos)
        for node in impassable_node.pred():
            self._updateVertex(node)

    def make_edge_impassable(self, impassable_edge):
        self._impassable_edges.add(impassable_edge)
        for node in impassable_edge:
            self._updateVertex(node)


class StateFactory(object):
    """Factory for creating or getting states."""
    def __init__(self, state_class, node_lookup_dict, valid_pos_lookup_func,
                 debug=False):
        self.state_class = state_class
        self.node_lookup_dict = node_lookup_dict
        self.valid_pos_lookup_func = valid_pos_lookup_func
        self.debug = debug

    def make_or_get_state_by_pos(self, pos):
        """Looks up a position in the dictionary, returns the state if the pos
        exists in the dictionary. Creates the state and adds it to the dict
        if it does not already exist, then returns it."""
        if self.debug:
            print "got request for pos %s" % (pos,)
        tmp_state = self.state_class(pos, (float("inf"), float("inf")))
        if tmp_state in self.node_lookup_dict:
            if self.debug:
                print "found state in dict"
            return self.node_lookup_dict[tmp_state]
        elif self.valid_pos_lookup_func(pos):
            if self.debug:
                print "didn't find state, making new one"
            new_s = self.state_class(pos, (float("inf"), float("inf")))
            new_s.set_node_lookup_dict(self.node_lookup_dict)
            new_s.set_valid_pos_lookup_func(self.valid_pos_lookup_func)
            new_s.set_state_factory(self)
            self.node_lookup_dict[new_s] = new_s
            return new_s
        else:
            # The requested state is not a valid position.
            return None


def fluid_is_valid(pos):
    """Determines whether a given position is valid or not."""
    return max(pos) <= 10 and min(pos) >= 0

def fluid_is_valid_2(pos):
    """Determines whether a given position is valid or not."""
    return min(pos) >= 0 and pos[0] <= 2 and pos[1] < 1 and pos[2] < 1


def test():
    """Tests the fluid routing. Also a helpful example of usage."""
    state_lookup_dict = {}
    fluid_state_factory = StateFactory(NodeState, state_lookup_dict,
                                       fluid_is_valid, debug=False)

    s_start = fluid_state_factory.make_or_get_state_by_pos((0, 0, 0))
    s_goal = fluid_state_factory.make_or_get_state_by_pos((2, 2, 2))

    flpa = FluidLPA(s_start, s_goal, state_lookup_dict)

    flpa.computeShortestPath()
    (path, cost) = flpa.getShortestPath()

    flpa.computeShortestPath()
    (path1, cost) = flpa.getShortestPath()

    flpa2 = copy.deepcopy(flpa)
    flpa2.make_node_impassable(
        flpa2.state_factory.make_or_get_state_by_pos((1, 1, 1)))

    flpa2.computeShortestPath()
    assert path1 != flpa2.getShortestPath()[0]

    flpa.computeShortestPath()
    assert path1 == flpa.getShortestPath()[0]

    for state in flpa.getShortestPath()[0]:
        print state.pos

    print ""

    for state in flpa2.getShortestPath()[0]:
        print state.pos

def test2():
    """Tests that fluid routing can deal with impassable routes."""
    state_lookup_dict = {}
    fluid_state_factory = StateFactory(NodeState, state_lookup_dict,
                                       fluid_is_valid_2, debug=False)

    s_start = fluid_state_factory.make_or_get_state_by_pos((0, 0, 0))
    s_goal = fluid_state_factory.make_or_get_state_by_pos((2, 0, 0))

    flpa = FluidLPA(s_start, s_goal, state_lookup_dict, debug=True)
    flpa.make_node_impassable(
        flpa.state_factory.make_or_get_state_by_pos((1, 0, 0)))

    flpa.computeShortestPath()
    print "computed shortest path"
    (path, cost) = flpa.getShortestPath()
    assert path is None
    assert cost == float("inf")

if __name__ == '__main__':
    test()
    # test()