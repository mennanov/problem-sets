# -*- coding: utf-8 -*-
from random import shuffle


class Graph(object):
    """
    Graph minimum cut search with the random contraction algorithm
    developed by Karger.
    The running time is O(E*E*M) where E is a number of vertices and M is the number of edges.
    This implementation handles undirected graphs only.
    """

    def __init__(self, vertices):
        self.edges = []
        self.vertices = len(vertices)
        # build edges from vertices
        for vertex, adjacent in vertices.items():
            for adj in adjacent:
                a = [vertex, adj]
                b = [adj, vertex]
                if a not in self.edges and b not in self.edges:
                    self.edges.append(a)

    def min_cut(self):
        """
        Randomized contraction algorithm for searching a minimum cut in a graph.
        """
        # the max possible number of min cuts in the graph
        tries = self.vertices * (self.vertices - 1) / 2
        min_cut = float('inf')
        # execute the min cut routine 'tries' times and choose the best min cut
        for _ in xrange(tries):
            # create a copy of edges list (deepcopy() is too slow)
            edges = []
            for e in self.edges:
                edges.append(e[:])
            shuffle(edges)
            m = self._min_cut(edges, self.vertices)
            if m < min_cut:
                min_cut = m
        return min_cut

    def _min_cut(self, edges, vertices):
        """
        Algorithm routine
        """
        # build edges from adjacent list
        while vertices > 2:
            # contract edge
            edge = edges.pop()
            # update related edges
            self_loops = []
            for e in edges:
                if edge[0] == e[0]:
                    e[0] = edge[1]
                elif edge[0] == e[1]:
                    e[1] = edge[1]
                # self loop check
                if e[0] == e[1]:
                    self_loops.append(e)
            # remove self loops
            for s in self_loops:
                edges.remove(s)
            vertices -= 1
        return len(edges)


def _build_edges(vertices):
    """
    Build edges from
    """
    edges = []
    for vertex, adjacent in vertices.items():
        for adj in adjacent:
            a = [vertex, adj]
            b = [adj, vertex]
            if a not in edges and b not in edges:
                edges.append(a)
    return edges


if __name__ == '__main__':
    vertices = dict([(1, [3, 2]), (3, [1, 2, 4]), (2, [1, 3, 4]), (4, [2, 3])])
    graph = Graph(vertices)
    assert graph.min_cut() == 2