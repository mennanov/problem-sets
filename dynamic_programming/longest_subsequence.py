# -*- coding: utf-8 -*-

"""
Goal: find the longest increasing or decreasing inconsequent subsequence in a given sequence.
For example: in a given sequence [5, 2, 8, 6, 3, 6, 9, 7]
the longest increasing subsequence is [2, 3, 6, 9]
"""
from other.graphs.graph import Graph
from graph_shortest_path import FindPathDP, Path


class LongestSequenceDP(object):
    """
    Longest subsequence searching with dynamic programming approach.
    We build a directed acyclic graph of all possible transitions from one number
    to another and find the longest path from any vertex to any vertex in this graph.
    Overall running time is linear in E (number of edges in a DAG),
    this is at most O(N^2) - worst case when the input array is sorted in increasing order.
    """

    def __init__(self, sequence):
        self.sequence = sequence
        # build a graph from that sequence
        graph_inc = Graph()
        graph_dec = Graph()
        k = len(self.sequence)
        for i in xrange(k):
            # only transitions from left to right
            for j in xrange(i, k):
                if sequence[j] > sequence[i]:
                    # increasing transition
                    graph_inc.add_edge(sequence[i], sequence[j])
                elif sequence[j] < sequence[i]:
                    # decreasing transition
                    graph_dec.add_edge(sequence[i], sequence[j])

        self.graph_inc = graph_inc
        self.graph_dec = graph_dec

    def increasing(self):
        """
        Find the longest increasing subsequence
        """
        longest_path = Path()
        # find the longest path from every vertex in the graph to any other vertex
        for v_from in self.graph_inc:
            fp = FindPathDP(self.graph_inc, v_from.name)
            for v_to in self.graph_inc[v_from.name].outgoing:
                if v_to != v_from:
                    lp = fp.longest_path(v_to.name)
                    # update the longest path so far
                    if lp > longest_path:
                        longest_path = lp
                        longest_path.start = v_from.name
        return [longest_path.start] + [x[0] for x in longest_path]

    def decreasing(self):
        """
        Find the longest decreasing subsequence
        """
        longest_path = Path()
        # find the longest path from every vertex in the graph to any other vertex
        for v_from in self.graph_dec:
            fp = FindPathDP(self.graph_dec, v_from.name)
            for v_to in self.graph_dec[v_from.name].outgoing:
                if v_to != v_from:
                    lp = fp.longest_path(v_to.name)
                    # update the longest path so far
                    if lp > longest_path:
                        longest_path = lp
                        longest_path.start = v_from.name
        return [longest_path.start] + [x[0] for x in longest_path]


if __name__ == '__main__':
    sequence = [5, 2, 8, 6, 3, 6, 9, 7]

    ls = LongestSequenceDP(sequence)
    assert ls.increasing() == [2, 3, 6, 9]
    assert ls.decreasing() == [8, 6, 3]