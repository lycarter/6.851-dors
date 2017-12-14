"""Routes multiple fluid channels simultaneously."""

import copy
import numpy as np
import lpa_fluid_router as flpa
import random
import lpa_math
import priority_queue as pq

class FLPA_BFS(object):
    """BFS Python implementation."""
    def __init__(self, desired_routes, valid_region_func, debug=False):
        """Args:
            desired_routes: List of (startPos, endPos)
            valid_region_func: Function taking a position as input and returning
                True or False depending on whether this position is in an
                allowed region.
        """

        # Initialize variables
        self.desired_routes = desired_routes
        self.debug = debug

        # Initialize starting FLPA
        flpa_list = []
        for route in desired_routes:
            state_lookup_dict = {}
            fluid_state_factory = flpa.StateFactory(
                flpa.NodeState, state_lookup_dict, valid_region_func)
            s_start = fluid_state_factory.make_or_get_state_by_pos(route[0])
            s_goal = fluid_state_factory.make_or_get_state_by_pos(route[1])

            route_flpa = flpa.FluidLPA(s_start, s_goal, state_lookup_dict)

            flpa_list.append(route_flpa)

        self.flpa_queue = pq.queue()
        self.flpa_queue.insert((-1,tuple(flpa_list)))

    def _check_edge_collision(self, edge_1, edge_2):
        a0 = np.array(edge_1[0].pos)
        a1 = np.array(edge_1[1].pos)
        b0 = np.array(edge_2[0].pos)
        b1 = np.array(edge_2[1].pos)
        if lpa_math.closest_distance_between_lines(a0, a1, b0, b1) < 0.8:
            if self.debug:
                print ('Edge collision detected, distance is %s' %
                    lpa_math.closest_distance_between_lines(a0, a1, b0, b1))
            return True
        return False


    def _check_collision_free(self, flpa_list, flpa_index_1, flpa_index_2,
                              path_1, path_2, flpa_cost):
        """Checks that path_1 and path_2 are collision-free. If they are not,
        calls a split method appropriately and returns False."""

        # check direct collisions
        for node in path_1:
            if node in path_2:
                if self.debug:
                    print "node overlap conflict at %s" % (node.pos,)
                self._split_flpa_pos(flpa_list, flpa_index_1, flpa_index_2,
                                     node.pos, flpa_cost)
                return False

        # check edge collisions
        edges_1 = [(path_1[i], path_1[i+1]) for i in range(len(path_1) - 1)]
        edges_2 = [(path_2[i], path_2[i+1]) for i in range(len(path_2) - 1)]
        for edge_1 in edges_1:
            for edge_2 in edges_2:
                if self._check_edge_collision(edge_1, edge_2):
                    if self.debug:
                        print ("edge conflict at (%s, %s), (%s, %s)" % 
                            (edge_1[0].pos, edge_1[1].pos, edge_2[0].pos,
                             edge_2[1].pos))
                    self._split_flpa_edge(flpa_list, flpa_index_1, flpa_index_2,
                                          edge_1, edge_2, flpa_cost)
                    return False

        # no collisions
        return True


    def _process_flpa_list(self, flpa_list):
        """Computes the shortest path for all of the FLPA's in flpa_list. Splits
        on a random bad position and returns None if the flpa_list is
        unsolvable. Returns a list of paths if the flpa_list is solvable."""

        paths = []
        total_flpa_cost = 0
        for route_flpa in flpa_list:
            if self.debug:
                print "Solving new FLPA"
            route_flpa.computeShortestPath()
            if self.debug: print "computed shortest path"
            (tmp_path, cost) = route_flpa.getShortestPath()
            if tmp_path is None:
                return (None, float("inf"))
            paths.append(tmp_path)
            total_flpa_cost += cost

        # collision check
        if self.debug:
            for path in paths:
                print "Potential path is:"
                for node in path:
                    print node.pos
        for i in range(len(paths)):
            for j in range(i+1, len(paths)):
                if self._check_collision_free(flpa_list, i, j, paths[i],
                                              paths[j], total_flpa_cost):
                    continue
                else:
                    return (None, float("inf"))

        return (paths, total_flpa_cost)


    def _split_flpa_edge(self, flpa_list, flpa_index_1, flpa_index_2, edge_1,
                         edge_2, cost):
        """Splits two routes at edge_1 and edge_2 respectively and appends the
        new search objects to the flpa_queue."""

        # split left
        left_flpa_list = copy.deepcopy(flpa_list)
        left_flpa_list[flpa_index_1].make_edge_impassable(edge_1)
        
        right_flpa_list = copy.deepcopy(flpa_list)
        right_flpa_list[flpa_index_2].make_edge_impassable(edge_2)

        self._queue_insert(left_flpa_list, right_flpa_list, cost)


    def _split_flpa_pos(self, flpa_list, flpa_index_1, flpa_index_2, bad_pos,
                        cost):
        """Splits two routes at bad_pos and appends the new search objects to
        the flpa_queue."""

        # split left
        left_flpa_list = copy.deepcopy(flpa_list)
        tmp_flpa = left_flpa_list[flpa_index_1]
        tmp_flpa.make_node_impassable(
            tmp_flpa.state_factory.make_or_get_state_by_pos(bad_pos))

        # split right
        right_flpa_list = copy.deepcopy(flpa_list)
        tmp_flpa = right_flpa_list[flpa_index_2]
        tmp_flpa.make_node_impassable(
            tmp_flpa.state_factory.make_or_get_state_by_pos(bad_pos))

        self._queue_insert(left_flpa_list, right_flpa_list, cost)

    def _queue_insert(self, l1, l2, cost):
        """Inserts l1 and l2 into the priority queue with appropriate cost.
        """

        self.flpa_queue.insert((cost, tuple(l1)))
        self.flpa_queue.insert((cost, tuple(l2)))


    def find_solution(self):
        minCost = float("inf")
        best = None
        while minCost > self.flpa_queue.topKey()[0]:
            tmp_flpa_list = self.flpa_queue.pop()[1]
            if self.debug:
                print("Starting new FLPA. The current queue length is %s" %
                      len(self.flpa_queue))
            (paths, totalcost) = self._process_flpa_list(tmp_flpa_list)
            minCost = min(minCost, totalcost)
            if minCost == totalcost:
                best = paths
                if self.debug: print("\t valid candidate solution")
        return (best, minCost)





def test_1():
    """Tests multi-object fluid routing."""
    route_1 = ((0, 0, 1), (2, 2, 1))
    route_2 = ((2, 0, 1), (0, 2, 1))
    routes = [route_1, route_2]

    def fluid_is_valid(pos):
        return max(pos) <= 2 and min(pos) >= 0

    bfs_obj = FLPA_BFS(routes, fluid_is_valid, debug=True)

    (paths, cost) = bfs_obj.find_solution()
    print "\n\n\n"
    for path in paths:
        for state in path:
            print state.pos
        print ""

def test_2():
    """Another test for multi-object fluid routing."""
    route_main = ((1, 0, 1), (1, 6, 1))
    route_cross_1 = ((0, 1, 1), (2, 1, 1))
    route_cross_2 = ((0, 2, 1), (2, 2, 1))
    route_cross_3 = ((0, 3, 1), (2, 3, 1))
    route_cross_4 = ((0, 4, 1), (2, 4, 1))
    route_cross_5 = ((0, 5, 1), (2, 5, 1))

    routes = [route_main, route_cross_5, route_cross_4, route_cross_3,
              route_cross_2, route_cross_1]

    def fluid_is_valid(pos):
        return max(pos) <= 10 and min(pos) >= 0

    bfs_obj = FLPA_BFS(routes, fluid_is_valid, debug=False)
    (paths, cost) = bfs_obj.find_solution()
    print "\n\n\n"
    for path in paths:
        for state in path:
            print state.pos
        print ""


if __name__ == '__main__':
    # test_1()
    # test_1() w/ debug: 0.354/0.292/0.172
    # test_1() wo debug: 0.235/0.232/0.132
    test_2()
    # test_2() w/ debug: 54.809/51.032/3.948
    # test_2() wo debug: 47.387/47.064/0.496