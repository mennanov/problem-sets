# -*- coding: utf-8 -*-
from Queue import PriorityQueue
from other.graphs.graph import EdgeWeightedGraph


class MSTPrim(object):
    """
    Lazy implementation of a minimum spanning tree Prim's algorithm which runs in O(MlogN)
    where M is a number of edges and N is a number of vertices.
    At each iteration it looks for a closest vertex (edge with a min-cost) and
    adds it to an MST using a cut property.
    To find the closest vertex we use a heap bases priority queue.
    We call it lazy because we don't remove obsolete edges from the queue: we just
    don't use them checking the constraints every time.
    """

    def __init__(self, graph):
        self.graph = graph
        # queue with edges haven't seen so far
        self.edges = PriorityQueue()
        # visited vertices so far
        self.visited = set()
        # total cost of the mst
        self.cost = 0
        # resulting set of edges of the mst
        self.mst = set()
        # pick a random vertex from a graph
        start = next(graph.vertices.itervalues())
        # "visit" this vertex
        self._visit(start)
        while not self.edges.empty() and len(self.visited) < len(self.graph):
            weight, edge = self.edges.get()
            if edge.vertex_from in self.visited and edge.vertex_to in self.visited:
                # leave that edge and don't add it to the mst since BOTH of the vertices are
                # already in the mst: they are already connected and adding this edge will cause a loop
                continue
            else:
                # add that edge to mst
                self.mst.add(edge)
                # increase the total cost of the mst
                self.cost += edge.weight
                if edge.vertex_from not in self.visited:
                    self._visit(edge.vertex_from)
                if edge.vertex_to not in self.visited:
                    self._visit(edge.vertex_to)

    def _visit(self, vertex):
        """
        Mark vertex as visited and also add all the outgoing edges to
        the priority queue.
        """
        self.visited.add(vertex)
        for edge in vertex.outgoing:
            if edge.vertex_to not in self.visited:
                # put the edge into pq with weight as a priority
                self.edges.put((edge.weight, edge))


if __name__ == '__main__':
    graph = EdgeWeightedGraph()
    edges = [(1, 2, 2474), (2, 4, -246), (4, 3, 640), (4, 5, 2088), (3, 6, 4586), (6, 5, 3966), (5, 1, -3824)]

    for edge in edges:
        graph.add_edge(edge[0], edge[1], edge[2])
        # add the backwards edge to simulate an undirected graph
        graph.add_edge(edge[1], edge[0], edge[2])

    mst = MSTPrim(graph)
    assert mst.cost == 2624
