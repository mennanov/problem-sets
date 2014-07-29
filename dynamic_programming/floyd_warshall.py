# -*- coding: utf-8 -*-

"""
Floyd-Warshall algorithm allows to compute all pairs shortest paths in a graph with negative edge costs.
It is also capable to detect negative cost cycles.
The running time is O(N^3), space required is O(N^2).
"""
from collections import defaultdict


class FloydWarshall(object):

    def __init__(self, graph):
        self.graph = graph
        # dictionary with all pairs distances
        self.dist = defaultdict(lambda: defaultdict(lambda: float('inf')))
        # reconstruction paths dictionary
        self.prev = defaultdict(lambda: defaultdict(lambda: None))
        # the shortest path distance in a graph: not required by the algorithm, just for fun
        self.min_dist = float('inf')

    def _set_min_dist(self, value):
        if value < self.min_dist:
            self.min_dist = value

    def run(self):
        # define default distances for every edge
        for edge in self.graph.iteredges():
            self.dist[edge.vertex_from.name][edge.vertex_to.name] = edge.weight
            # update the min dist
            self._set_min_dist(edge.weight)
            self.prev[edge.vertex_from.name][edge.vertex_to.name] = edge.vertex_to
            self.dist[edge.vertex_from.name][edge.vertex_from.name] = 0
            self.dist[edge.vertex_to.name][edge.vertex_to.name] = 0

        for k in self.graph:
            for i in self.graph:
                for j in self.graph:
                    if self.dist[i.name][k.name] + self.dist[k.name][j.name] < self.dist[i.name][j.name]:
                        # found new shorter path from i to j
                        self.dist[i.name][j.name] = self.dist[i.name][k.name] + self.dist[k.name][j.name]
                        self._set_min_dist(self.dist[i.name][j.name])
                        self.prev[i.name][j.name] = self.prev[i.name][k.name]

        # check for the negative cost cycles
        for i in self.graph:
            if self.dist[i.name][i.name] < 0:
                raise RuntimeError('Graph has a negative cost cycle')

    def path(self, from_name, to_name):
        """
        Reconstruct the shortest path
        """
        path = [self.graph[from_name]]
        predecessor = self.prev[from_name][to_name]
        while predecessor is not None:
            path.append(predecessor)
            predecessor = self.prev[predecessor.name][to_name]

        return path


if __name__ == '__main__':
    from other.graphs.graph import EdgeWeightedGraph

    edges = [
        ('s', 'v', 2),
        ('x', 's', -3),
        ('v', 'w', 2),
        ('x', 't', 4),
        ('v', 'x', 1),
        ('w', 't', 3),
    ]
    graph = EdgeWeightedGraph()
    for edge in edges:
        graph.add_edge(edge[0], edge[1], edge[2])

    fw = FloydWarshall(graph)
    fw.run()
    assert fw.dist['s']['t'] == 7