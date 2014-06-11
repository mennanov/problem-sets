# -*- coding: utf-8 -*-
from other.graphs.graph import EdgeWeightedGraph, Vertex


class IndexedPriorityQueue(object):
    """
    Indexed priority queue which allows to update the priority
    of an arbitrary element in O(LogN) time.
    It keeps the extra dictionary with indexes of each element.
    """

    def __init__(self):
        self.indexes = {}
        self.keys = []
        self.data = []

    def __setitem__(self, key, item):
        if key in self.indexes:
            # remove existing item
            self.__delitem__(self.indexes[key])
        # add new item
        self.data.append(item)
        index = len(self) - 1
        self.keys.append(key)
        self.indexes[key] = index
        # put the item into the proper place and update indexes
        self._siftup(index)

    def get(self):
        """
        Removes the first element from the heap and returns it
        """
        return self.__delitem__(0)

    def __delitem__(self, k):
        """
        Delete item from the heap by its index
        """
        j = len(self) - 1
        # update keys
        self.indexes[self.keys[k]], self.indexes[self.keys[j]] = self.indexes[self.keys[j]], self.indexes[self.keys[k]]
        self.keys[k], self.keys[j] = self.keys[j], self.keys[k]
        del self.indexes[self.keys[j]]
        self.keys.pop()
        # move items
        self.data[k], self.data[j] = self.data[j], self.data[k]
        item = self.data.pop()
        self._siftdown(k)
        return item

    def _siftup(self, k):
        while k > 0 and self.data[k] < self.data[k // 2]:
            # update keys
            self.indexes[self.keys[k]], self.indexes[self.keys[k // 2]] = self.indexes[self.keys[k // 2]], self.indexes[
                self.keys[k]]
            self.keys[k], self.keys[k // 2] = self.keys[k // 2], self.keys[k]
            # move items
            self.data[k], self.data[k // 2] = self.data[k // 2], self.data[k]
            k //= 2

    def _siftdown(self, k):
        while k * 2 + 1 < len(self):
            j = k * 2 + 1
            if j + 1 < len(self) and self.data[j + 1] < self.data[j]:
                j += 1
            if self.data[k] <= self.data[j]:
                break
            else:
                # update keys
                self.indexes[self.keys[k]], self.indexes[self.keys[j]] = self.indexes[self.keys[j]], self.indexes[
                    self.keys[k]]
                self.keys[k], self.keys[j] = self.keys[j], self.keys[k]
                # move items
                self.data[k], self.data[j] = self.data[j], self.data[k]
            k = j

    def __nonzero__(self):
        return len(self) > 0

    def __len__(self):
        return len(self.data)


class DijkstraSP(object):
    """
    Dijkstra shortest path algorithm which runs O(MLogN) in this implementation (the best possible time).
    Running time depends on how fast the 'closest' vertex is found.
    Here we use indexed priority queue to achieve O(LogN) time to find the 'closest' vertex.
    """

    def __init__(self, graph, start):
        self.graph = graph
        self.start = self.graph[start]
        # minimum priority queue
        self.pq = IndexedPriorityQueue()
        self.start.distance = 0
        # add starting vertex to the queue
        self.pq[self.start.name] = self.start
        while self.pq:
            vertex = self.pq.get()
            # relax all the outgoing adjacent vertices
            for v, weight in vertex.outgoing:
                self._relax(vertex, v, weight)

    def _relax(self, v_from, v_to, weight):
        """
        Update the distance to the vertex if it is better that we already know
        """
        if v_from.distance + weight < v_to.distance:
            v_to.distance = v_from.distance + weight
            v_to.prev = v_from
            # update the priority queue
            self.pq[v_to.name] = v_to

    def dist_to(self, v):
        return self.graph[v].distance

    def path_to(self, v):
        """
        Get the full path from starting vertex to that one
        """
        path = []
        while v != self.start.name:
            path.append(self.graph[v].name)
            v = self.graph[v].prev.name
        return reversed(path)


if __name__ == '__main__':
    graph = EdgeWeightedGraph(Vertex)
    edges = [(1, 2, 7), (1, 3, 9), (1, 6, 14), (2, 1, 7), (2, 3, 10), (2, 4, 15), (3, 1, 9), (3, 2, 10), (3, 4, 11),
             (3, 6, 2), (4, 2, 15), (4, 3, 11), (4, 5, 6), (5, 4, 6), (5, 6, 9), (6, 1, 14), (6, 3, 2), (6, 5, 9)]

    for edge in edges:
        graph.add_edge(edge[0], edge[1], edge[2])

    sp = DijkstraSP(graph, 1)
    assert sp.dist_to(6) == 11