# -*- coding: utf-8 -*-

"""
Johnson algorithm combines Bellman-Ford and Dijkstra's algorithms to compute all pairs shortest paths.
The key idea is to modify a graph in a special way such as it will not have negative edges.
Bellman-Ford algorithm is used in this step by adding a source auxiliary vertex connected to every vertex in a graph.
When we finish the Bellman-Ford algorithm we can safely execute Dijkstra algorithm for every vertex in a graph.
The running time is O(MNLogN) which is derived from: O(N) for adding an aux vertex, O(MN) for Bellman-Ford execution,
O(M) to modify each edge in a graph with a new weight, O(NMLogN) - N times Dijkstra, O(N^2) - work per u-v pair.
Johnson algorithm runs faster in sparse graphs than a Floyd-Warshall algorithms.
"""
from bellman_ford import BellmanFord
from greedy_algorithms.graph_shortest_paths import DijkstraSP


class Johnson(object):
    def __init__(self, graph):
        self.graph = graph
        # distances computed in the modified graph
        self.modified_dist = {}
        # distances obtained by the Bellman-Ford algorithm
        self.bf_dist = {}
        # path reconstruction dictionary
        self.prev = {}

    def run(self):
        # add aux vertex
        for v in self.graph:
            self.graph.add_edge('aux', v.name, 0)
        # run Bellman-Ford algorithm for that vertex
        bf = BellmanFord(self.graph, 'aux')
        bf.run()
        # update graph edges
        for edge in self.graph.iteredges():
            edge.weight = edge.weight + bf.dist[edge.vertex_from.name] - bf.dist[edge.vertex_to.name]
        # keep the Bellman-Ford distances because we will need it to return real distances from s to t
        self.bf_dist = bf.dist
        # run Dijkstra algorithm for every vertex
        for vertex in self.graph:
            if vertex.name != 'aux':
                dj = DijkstraSP(self.graph, vertex.name)
                self.modified_dist[vertex.name] = dj.distance
                self.prev[vertex.name] = dj.prev

    def shortest_distance(self):
        result = float('inf')
        for i in self.graph:
            for j in self.graph:
                if i != j and 'aux' not in (i.name, j.name):
                    d = self.dist(i.name, j.name)
                    if d < result:
                        result = d
        return result

    def dist(self, from_name, to_name):
        """
        Compute the real distance as it was in the original graph
        """
        return self.modified_dist[from_name][to_name] - self.bf_dist[from_name] + self.bf_dist[to_name]

    def path(self, from_name, to_name):
        """
        Reconstruct the shortest path
        """
        path = [self.graph[to_name]]
        predecessor = self.prev[from_name][to_name]
        while predecessor.name != from_name:
            path.append(predecessor)
            predecessor = self.prev[from_name][predecessor.name]

        path.append(self.graph[from_name])
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

    jh = Johnson(graph)
    jh.run()
    assert jh.shortest_distance() == -3
