# -*- coding: utf-8 -*-

"""
Compute the max-spacing for k-clustering in a graph.
The algorithm is built on Kruskal's minimum spanning tree algorithm:
0. define the initial number of clusters as the number of vertices in a graph
1. sort all the edges in a graph in an increasing order of weight
2. iterate over the list of the edges:
3. "merge" two vertices by fusing them in a union-find data structure if this edge does not create a cycle
4. decrement the number of cluster by one
5. repeat until we get k clusters
"""
from other.graphs.graph import EdgeWeightedGraph
from other.union_find import UnionFind


class Clustering(object):
    """
    Clustering algorithm based on Kruskal's MST algorithm.
    The running time of this algorithm is O(MLogN)
    """

    def __init__(self, graph):
        self.graph = graph
        self.uf = UnionFind()

    def max_space(self, k):
        """
        Perform a max-space clustering until we get k clusters.
        """
        # set the initial number of clusters to the number of vertices (each vertex is a cluster by itself)
        clusters = len(self.graph)
        # sort edges by weight
        edges = sorted(self.graph.iteredges())
        for edge in edges:
            if clusters > k:
                # check for a cycle
                if self.uf.connected(edge.vertex_from, edge.vertex_to):
                    continue
                else:
                    # merge these vertices into a single cluster
                    self.uf.union(edge.vertex_from, edge.vertex_to)
                    clusters -= 1
            else:
                # check if the edge is an internal to the already formed clusters
                if self.uf.connected(edge.vertex_from, edge.vertex_to):
                    continue
                else:
                    return edge.weight

    def max_k(self, spacing):
        """
        Find the largest number of clusters such that there is a k-clustering with spacing at least 'spacing'
        """
        # set the initial number of clusters to the number of vertices (each vertex is a cluster by itself)
        clusters = len(self.graph)
        # sort edges by weight
        edges = sorted(self.graph.iteredges())
        for edge in edges:
            if edge.weight < spacing:
                # check for a cycle
                if self.uf.connected(edge.vertex_from, edge.vertex_to):
                    continue
                else:
                    # merge these vertices into a single cluster
                    self.uf.union(edge.vertex_from, edge.vertex_to)
                    clusters -= 1
            else:
                # check if the edge is an internal to the already formed clusters
                if self.uf.connected(edge.vertex_from, edge.vertex_to):
                    continue
                else:
                    return clusters

        return 1


if __name__ == '__main__':
    graph = EdgeWeightedGraph()
    edges = [(1, 2, 134365),
             (1, 3, 847434),
             (1, 4, 763775),
             (1, 5, 255070),
             (1, 6, 495436),
             (1, 7, 449492),
             (1, 8, 651593),
             (1, 9, 788724),
             (1, 10, 93860),
             (2, 3, 28348),
             (2, 4, 835766),
             (2, 5, 432768),
             (2, 6, 762281),
             (2, 7, 2107),
             (2, 8, 445388),
             (2, 9, 721541),
             (2, 10, 228763),
             (3, 4, 945271),
             (3, 5, 901428),
             (3, 6, 30590),
             (3, 7, 25446),
             (3, 8, 541413),
             (3, 9, 939150),
             (3, 10, 381205),
             (4, 5, 216600),
             (4, 6, 422117),
             (4, 7, 29041),
             (4, 8, 221692),
             (4, 9, 437888),
             (4, 10, 495813),
             (5, 6, 233085),
             (5, 7, 230867),
             (5, 8, 218782),
             (5, 9, 459604),
             (5, 10, 289782),
             (6, 7, 21490),
             (6, 8, 837578),
             (6, 9, 556455),
             (6, 10, 642295),
             (7, 8, 185907),
             (7, 9, 992544),
             (7, 10, 859947),
             (8, 9, 120890),
             (8, 10, 332696),
             (9, 10, 721485)]
    for edge in edges:
        graph.add_edge(*edge)

    c = Clustering(graph)
    assert c.max_space(4) == 134365