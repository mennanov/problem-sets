# -*- coding: utf-8 -*-

"""
It is a reversed problem of a clustering:
what is the largest value of k such that there is a k-clustering with spacing at least s?
Imagine that we have a big graph.
So big, in fact, that the distances (i.e., edge costs) are only defined implicitly,
rather than being provided as an explicit list.
For example, we havea string "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1"
which denotes the 24 bits associated with some node.
The distance between two nodes u and v in this problem is defined as the Hamming distance:
the number of differing bits between the two nodes' labels.
For example, the Hamming distance between the 24-bit label of the node above and the label
"0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3 (since they differ in the 3rd, 7th, and 21st bits).
In this approach can not examine each pair of nodes since it will run quadratic time and we can not accept this
on a huge graph.
Instead we will build a Huffman tree with all the nodes, then for each node we will be able to find all the nodes
with the Humming distance <= needed (closest nodes) in a sublinear time per each call.
Though in the worst case it may still run quadratic, in practice it is fast enough.
"""
from other.graphs.graph import EdgeWeightedGraph
from clustering import Clustering


class HuffmanTree(object):

    class Node(object):

        def __init__(self, value=None):
            # only a leaf node may have a value
            self.value = value
            # pointer to the left node
            self.left = None
            # pointer to the right node
            self.right = None

        def __repr__(self):
            return u'Node({})'.format(repr(self.value))

    def __init__(self):
        self.root = self.Node()

    def add(self, value, bits):
        """
        Add a new leaf node in a tree using provided bits (a list of 0 and 1)
        """
        # print value, bits
        self.root = self._add(value, bits, self.root)

    def _add(self, value, bits, node):
        if node is None:
            if len(bits) == 0:
                return self.Node([value])
            else:
                return self._add(value, bits, self.Node())

        if len(bits) == 0:
            # duplicates are also accepted
            node.value.append(value)
            return node

        if bits[0] == 0:
            # go left
            node.left = self._add(value, bits[1:], node.left)
        else:
            # go right
            node.right = self._add(value, bits[1:], node.right)
        return node

    def relative_nodes(self, bits, humming_distance):
        """
        Find all the nodes which humming distance is less or equal to the given Humming distance
        """
        for node in self._dfs(bits, humming_distance, self.root, len(bits)):
            yield node

    def _dfs(self, bits, distance_needed, node, bit_length, distance_so_far=0, bit_position=0):
        if node is None:
            return
        if node.value and distance_so_far <= distance_needed:
            yield node, distance_so_far

        if bit_position >= bit_length:
            return

        # go left
        dist = distance_so_far + 1 if bits[bit_position] == 1 else distance_so_far
        if dist <= distance_needed:
            for n in self._dfs(bits, distance_needed, node.left, bit_length, dist, bit_position + 1):
                yield n

        # go right
        dist = distance_so_far + 1 if bits[bit_position] == 0 else distance_so_far
        if dist <= distance_needed:
            for n in self._dfs(bits, distance_needed, node.right, bit_length, dist, bit_position + 1):
                yield n


if __name__ == '__main__':
    tree = HuffmanTree()
    nodes = dict()
    with open('clustering.txt', 'r') as fp:
        # fill in the Huffman tree
        for i, line in enumerate(fp):
            if i > 0:
                bits = [int(x) for x in line.split()]
                tree.add(i, bits)
                nodes[i] = bits

    graph = EdgeWeightedGraph()

    for node, bits in nodes.iteritems():
        # for this node add its edges to the graph with weights <= 3 only
        # to be able to find all these edges we look them up in a Huffman tree:
        # if we look at each pair of nodes the program will be too slow (quadratic)
        for r_nodes, distance in tree.relative_nodes(bits, 3):
            for n in r_nodes.value:
                graph.add_edge(node, n, distance)

    c = Clustering(graph)
    assert c.max_k(3) == 989