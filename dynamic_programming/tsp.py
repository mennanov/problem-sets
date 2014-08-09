# -*- coding: utf-8 -*-

"""
A traveling salesman is getting ready for a big sales tour. Starting at his hometown, suitcase
in hand, he will conduct a journey in which each of his target cities is visited exactly once
before he returns home. Given the pairwise distances between cities, what is the best order
in which to visit them, so as to minimize the overall distance traveled?
"""
import math
from collections import defaultdict
from other.graphs.graph import EdgeWeightedGraph
from graph_shortest_path import Path, memoize
from combinatorics.generate_combinations import xcombinations_bin, xcombinations_lex


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


class TSP(object):
    """
    Academical implementation of the TSP problem using dynamic programming.
    The running time is O(N^2 * 2^N). It uses bit vectors instead of sets (of frozensets) and a list instead
    of a dictionary to avoid MemoryError on large input sets (> 25 vertices).
    Also, bit vectors usage decently improves the actual running time because operations with sets sometimes take O(N).
    """

    def __init__(self, graph, start_name):
        self.graph = graph
        # 2-d array of distances for set of vertices and the destination vertex
        self.dist = [None] * (2 ** len(self.graph))
        # startint point
        self.start = start_name
        # vertices keys
        self.vertices = self.graph.vertices.keys()

    def _vertices_combinations(self, length, start=0):
        """
        Generate combinations of vertices of a given length as a bit vector.
        """
        if length == 0:
            yield 0
        else:
            for i in xrange(start, len(self.vertices)):
                for subcomb in self._vertices_combinations(length - 1, i + 1):
                    yield (1 << i) | subcomb

    def _int_combinations(self, length):
        n = 2 ** length
        for i in xrange(n):
            yield i

    def run(self):
        # fill in the base cases when the destination is the source vertex
        for s in self._int_combinations(len(self.vertices)):
            if s == (1 << self.start):
                self.dist[s] = [0] + [float('inf')] * (len(self.vertices) - 1)
            elif s == 0:
                self.dist[s] = [0] * len(self.vertices)
            else:
                self.dist[s] = [float('inf')] * len(self.vertices)

        for m in xrange(1, len(self.graph) + 1):
            for s in self._vertices_combinations(m):
                if s & (1 << self.start):
                    for j in xrange(s.bit_length()):
                        bit = s >> j & 1
                        if bit and j != self.start:
                            best = float('inf')
                            for edge in self.graph[self.vertices[j]].incoming:
                                # set with removed j
                                sj = s & ~(1 << j)
                                dist = self.dist[sj][edge.vertex_from.name] + edge.weight
                                if dist < best:
                                    best = dist
                            self.dist[s][self.graph[self.vertices[j]].name] = best
        # search for the best incoming route to the starting point
        best = float('inf')
        for edge in self.graph[self.start].incoming:
            d = self.dist[-1][edge.vertex_from.name] + edge.weight
            if d < best:
                best = d
        return best


if __name__ == '__main__':
    # edges = [('a', 'b', 2), ('a', 'c', 2), ('a', 'd', 1), ('a', 'e', 4), ('b', 'c', 3),
    #          ('b', 'e', 3), ('b', 'd', 2), ('c', 'd', 2), ('c', 'e', 2), ('e', 'd', 4)]
    # graph = EdgeWeightedGraph()
    # for edge in edges:
    #     graph.add_edge(edge[0], edge[1], edge[2])
    #     # backward edge since graph is undirected
    #     graph.add_edge(edge[1], edge[0], edge[2])
    # tsp_dp = TSPDP(graph)
    # tsp_bf = TSPBF(graph)
    # assert tsp_dp.path('a') == tsp_bf.path('a')
    graph = EdgeWeightedGraph()
    points = []
    with open('tsp.txt', 'r') as fp:
        header = fp.readline()
        for line in fp:
            point = line.split()
            points.append((float(point[0]), float(point[1])))

    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            if i != j:
                dist = math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
                graph.add_edge(i, j, dist)
                # graph.add_edge(j, i, dist)
    tsp = TSP(graph, 0)
    print tsp.run()



