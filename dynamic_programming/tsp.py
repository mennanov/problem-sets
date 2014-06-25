# -*- coding: utf-8 -*-

"""
A traveling salesman is getting ready for a big sales tour. Starting at his hometown, suitcase
in hand, he will conduct a journey in which each of his target cities is visited exactly once
before he returns home. Given the pairwise distances between cities, what is the best order
in which to visit them, so as to minimize the overall distance traveled?
"""
from other.graphs.graph import EdgeWeightedGraph
from graph_shortest_path import Path, memoize


class TSPDP(object):
    """
    Travelling salesman problem: dynamic programming approach.
    Running time is O(n^2*2^n) since there are at most 2^n*n subproblems,
    and each takes linear time to solve.
    """

    def __init__(self, graph):
        self.graph = graph

    @memoize
    def path(self, source, start=None, visited=None):
        # if we came back to the source vertex
        if start == source:
            # we may come back to the source vertex only if all
            # the vertices have been already visited once
            if frozenset(self.graph.vertices.keys()) == visited:
                return Path()
            else:
                # otherwise we miss some vertices out of the route, so
                # this is a bad path and we give it an infinite weight
                return Path(float('inf'))
        elif start is None:
            start = source

        if visited is None:
            visited = frozenset()
        # the best possible path so far
        best = Path(float('inf'))
        # run depth-first search from the start vertex
        for v, weight in self.graph[start].outgoing:
            if v.name not in visited:
                path = self.path(source, v.name, visited | frozenset([v.name])).copy()
                # add the current edge to that path
                path.add(v, weight)
                if path < best:
                    best = path
        # return the shortest path
        return best


class TSPBF(object):
    """
    Travelling salesman problem: brute force approach.
    Running time is O(n!) since there are n! possible ways of visiting each vertex.
    This is much slower than dynamic programming approach, so it should not be used in practice.
    """

    def __init__(self, graph):
        self.graph = graph

    def path(self, source):
        best = Path(float('inf'))
        for path in self._dfs(source):
            if path < best:
                best = path
        return best

    def _dfs(self, source, start=None, visited=None):
        # if we came back to the source vertex
        if start == source:
            # we may come back to the source vertex only if all
            # the vertices have been already visited once
            if frozenset(self.graph.vertices.keys()) == visited:
                yield Path()
            else:
                # otherwise we miss some vertices out of the route, so
                # this is a bad path and we give it an infinite weight
                yield Path(float('inf'))
        elif start is None:
            start = source

        if visited is None:
            visited = frozenset()
        # run depth-first search from the start vertex
        for v, weight in self.graph[start].outgoing:
            if v.name not in visited:
                for subpath in self._dfs(source, v.name, visited | frozenset([v.name])):
                    # add the current edge to that path
                    subpath.add(v, weight)
                    yield subpath


if __name__ == '__main__':
    edges = [('a', 'b', 2), ('a', 'c', 2), ('a', 'd', 1), ('a', 'e', 4), ('b', 'c', 3),
             ('b', 'e', 3), ('b', 'd', 2), ('c', 'd', 2), ('c', 'e', 2), ('e', 'd', 4)]
    graph = EdgeWeightedGraph()
    for edge in edges:
        graph.add_edge(edge[0], edge[1], edge[2])
        # backward edge since graph is undirected
        graph.add_edge(edge[1], edge[0], edge[2])
    tsp_dp = TSPDP(graph)
    tsp_bf = TSPBF(graph)
    assert tsp_dp.path('a') == tsp_bf.path('a')


