# -*- coding: utf-8 -*-

"""
Bellman-Ford algorithm for computing the single-source shortest paths in graph which may have
negative edge costs. If the graph has a negative cost cycle then it should report about it and terminate.
The running time is O(mn) and the space required is O(n).
"""
from collections import defaultdict


class BellmanFord(object):

    def __init__(self, graph, source_name):
        self.graph = graph
        # path reconstruction dictionary
        self.prev = defaultdict(lambda: None)
        # distance from the source vertex to every vertex in the graph
        self.dist = defaultdict(lambda: float('inf'))
        # source vertex
        self.source = self.graph[source_name]
        # distance to the source itself is zero
        self.dist[self.source.name] = 0

    def run(self):
        n = len(self.graph)
        # we run the algorithm n times to be able to detect negative cycles in the last iteration
        for i in xrange(n + 1):
            for vertex in self.graph:
                # iterate over every incoming edge of this vertex
                for edge in vertex.incoming:
                    if edge.weight + self.dist[edge.vertex_from.name] < self.dist[vertex.name]:
                        if i == n:
                            # during the last iteration improvement may be only if there is a negative cycle
                            raise RuntimeError('Graph has a negative cost cycle')
                        # shorter path is found: update dist and prev
                        self.dist[vertex.name] = edge.weight + self.dist[edge.vertex_from.name]
                        self.prev[vertex.name] = edge.vertex_from

    def path_to(self, vertex_name):
        """
        Reconstruct the shortest path to the vertex
        """
        path = []
        predecessor = self.prev[vertex_name]
        while predecessor is not None:
            path.append(predecessor)
            predecessor = self.prev[predecessor.name]

        return reversed(path)


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

    bf = BellmanFord(graph, 's')
    bf.run()
    assert bf.dist['t'] == 7

