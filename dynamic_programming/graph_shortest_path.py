# -*- coding: utf-8 -*-
from other.graph import EdgeWeightedGraph


class Path(object):
    """
    Graph path
    """

    def __init__(self, weight=0):
        # the route from starting vertex to the finish
        self.edges = []
        # overall weight
        self.weight = weight

    def __len__(self):
        return len(self.edges)

    def add(self, vertex_to, weight):
        self.edges.append((vertex_to, weight))
        self.weight += weight

    def __cmp__(self, other):
        if self.weight > other.weight:
            return 1
        elif self.weight < other.weight:
            return -1
        else:
            return 0

    def __str__(self):
        return str(self.edges)

    def __repr__(self):
        return str(self.edges)


class FindPathDP(object):
    """
    Exploring the shortest path with a dynamic programming approach.
    We recursively iterate over the incoming adjacent vertices of the needed vertex
    and at every recursion call find the best sub-route.
    """

    def __init__(self, graph, start):
        self.graph = graph
        self.start = start

    def shortest_path(self, to):
        """
        Shortest path. We use the 'min' function to compare paths
        """
        return self._dfs(to, min)

    def longest_path(self, to):
        """
        Longest path. We use the 'max' function to compare paths
        """
        return self._dfs(to, max)

    def _dfs(self, to, choose):
        """
        Simplified depth-first search without marking vertices as 'visited'
        Iterate over vertices in a reversed order (backward edges)
        """
        if to == self.start:
            # reached the starting point
            return Path()
        if not self.graph[to].incoming:
            # the last vertex, no where to go - it is a wrong way
            s = [float('inf'), float('-inf')]
            s.remove(choose(float('inf'), float('-inf')))
            return Path(s[0])
        paths = []
        for v, weight in self.graph[to].incoming:
            c = self._dfs(v.name, choose)
            c.add(to, weight)
            paths.append(c)
        return choose(paths)

if __name__ == '__main__':
    graph = EdgeWeightedGraph()
    edges = [('s', 'a', 1), ('s', 'c', 2), ('c', 'd', 3), ('c', 'a', 4), ('a', 'b', 6), ('b', 'd', 1), ('b', 'e', 2),
             ('d', 'e', 1), ('f', 'c', 3)]
    for edge in edges:
        graph.add_edge(edge[0], edge[1], edge[2])

    path = FindPathDP(graph, 's')
    assert path.shortest_path('d').weight == 5
    assert path.longest_path('d').weight == 13
