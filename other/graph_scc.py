# -*- coding: utf-8 -*-

"""
This implementation of Kosoraju-Sharir algorithms uses
recursive depth-first search which inevitably will hit the
maximum recursion depth limit with large data sets.
One possible work-around is to increase this limit by adding
    import sys
    sys.setrecursionlimit(2**20)
but ideally these recursive methods should be rewritten so that
it would not use any recursion (the implementation is similar to breadth-first search, but instead
of using queue you should use a stack), though the correct implementation is quite tricky.
"""
from graph import Graph


class SCC(object):
    """
    Directed graph Kosoraju-Sharir strongly connected components algorithm.
    It works this way: at first we run depth-first-search in a reversed graph (reversed edges) to
    determine the right order of vertices to iterate through the second depth-first-search which will
    give us strongly connected components of the graph.
    """

    def __init__(self, graph):
        self.graph = graph
        # graph vertices in reversed topological order
        # after the first reversed depth-first search
        self.order = []
        self.visited = set()
        # the list with all found scc
        self.scc = []

    def run(self):
        """
        Run the algorithm
        """
        self._first_run()
        self._second_run()

    def _first_run(self):
        """
        Run the dfs in a reversed graph.
        This must be called before the second run
        """
        for k in reversed(self.graph):
            v = self.graph[k]
            if v not in self.visited:
                self.rdfs(v)

    def _second_run(self):
        """
        Runs the dfs in a special order in order
        to discover all the SCC
        """
        self.visited = set()
        for i in xrange(len(self.order)):
            vertex = self.order.pop()
            if vertex not in self.visited:
                self.scc.append(self.dfs(vertex))

    def rdfs(self, vertex):
        """
        Run depth-first search in a reversed graph
        """
        self.visited.add(vertex)
        # for every incoming vertex of that vertex
        for v in self.graph[vertex.name].incoming:
            if v not in self.visited:
                self.rdfs(v)
        # add vertex to the order list
        self.order.append(vertex)

    def dfs(self, vertex):
        """
        Run depth-first search in a graph
        """
        self.visited.add(vertex)
        scc = []
        # for every incoming vertex of that vertex
        for v in self.graph[vertex.name].outgoing:
            if v not in self.visited:
                scc += self.dfs(v)
        # NOTE: if you only need to calculate the amount of vertices in SCC without actually
        # storing the vertices then set scc to 0 and change the next line to
        # return scc + 1
        # it will save you from a segmentation fault in a large data set
        return scc + [vertex]


if __name__ == '__main__':
    graph = Graph()
    edges = [[1, 4], [2, 8], [3, 6], [4, 7], [5, 2], [6, 9], [7, 1], [8, 5], [8, 6], [9, 7], [9, 3]]
    for edge in edges:
        graph.add_edge(edge[0], edge[1])

    scc = SCC(graph)
    scc.run()
    assert [len(x) for x in scc.scc] == [3, 3, 3]