# -*- coding: utf-8 -*-
from other.graphs.graph import EdgeWeightedGraph


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

    def __iter__(self):
        return iter(self.edges)

    def copy(self):
        """
        Create a deepcopy of the object
        """
        path = Path(self.weight)
        for v, weight in self.edges:
            path.edges.append((v, weight))
        return path

    def __str__(self):
        return 'Path: {}'.format(str(self.edges))

    def __repr__(self):
        return 'Path({}) at {}'.format(str(self.weight), str(hex(id(self))))

    def __eq__(self, other):
        return self.edges == other.edges


def memoize(func):
    """
    Simple memoization decorator (it does not handle kwargs since we don't need them)
    """
    cache = dict()

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    return wrapper


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

    @memoize
    def _dfs(self, to, choose):
        """
        Simplified depth-first search without marking vertices as 'visited'.
        Instead of marking vertices as visited we save already known paths by using @memoize decorator,
        it requires some extra memory but it is totally worth it.
        The running time in that case is O(E + V) where E is a number of edges and V - vertices in a DAG.
        If we don't use a @memoize decorator the algorithm will wind up in exponential time since we will
        go through already explored paths again and again.
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
        for vertex in self.graph[to].incoming:
            # edge weighted graph has a tuple, a simple graph doesn't
            if isinstance(vertex, tuple):
                v, weight = vertex
            else:
                v = vertex
                weight = 1
            # need to create a copy of that path since we don't want to modify it.
            # This is very important if we use memoize decorator since it stores all the paths in a dictionary
            c = self._dfs(v.name, choose).copy()
            c.add(to, weight)
            paths.append(c)
        return choose(paths)


class FindPathBF(object):
    """
    Exploring the shortest path with a brute force approach.
    We find all the possible paths and choose the best one of them.
    It has an exponential running time complexity.
    """

    def __init__(self, graph, start):
        self.graph = graph
        self.start = start

    def shortest_path(self, to):
        """
        Shortest path. We use the 'min' function to compare paths
        """
        return min(self._dfs(to, float('inf')))

    def longest_path(self, to):
        """
        Longest path. We use the 'max' function to compare paths
        """
        return max(self._dfs(to, float('-inf')))

    def _dfs(self, to, inf):
        """
        Simplified depth-first search without marking vertices as 'visited'
        Iterate over vertices in a reversed order (backward edges)
        """
        if to == self.start:
            # reached the starting point
            return [Path()]
        if not self.graph[to].incoming:
            # the last vertex, no where to go - it is a wrong way
            return [Path(inf)]
        paths = []
        for v, weight in self.graph[to].incoming:
            for c in self._dfs(v.name, inf):
                c.add(to, weight)
                paths.append(c)
        return paths


if __name__ == '__main__':
    graph = EdgeWeightedGraph()
    edges = [('s', 'a', 1), ('s', 'c', 2), ('c', 'd', 3), ('c', 'a', 4), ('a', 'b', 6), ('b', 'd', 1), ('b', 'e', 2),
             ('d', 'e', 1), ('f', 'c', 3)]
    for edge in edges:
        graph.add_edge(edge[0], edge[1], edge[2])

    path = FindPathDP(graph, 's')
    assert path.shortest_path('d').weight == 5
    assert path.longest_path('d').weight == 13
    path = FindPathBF(graph, 's')
    assert path.shortest_path('d').weight == 5
    assert path.longest_path('d').weight == 13
