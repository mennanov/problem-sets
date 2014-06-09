# -*- coding: utf-8 -*-

"""
Graph API
"""
from collections import OrderedDict


class Vertex(object):
    """
    Graph vertex
    """

    def __init__(self, name):
        self.name = name
        # outgoing edges (list of vertices)
        self.outgoing = []
        # incoming edges (list of vertices)
        self.incoming = []

    def __repr__(self):
        return u'Vertex({})'.format(repr(self.name))


class Graph(object):
    """
    Directed graph API
    """
    def __init__(self):
        self.vertices = OrderedDict()

    def add_edge(self, name1, name2):
        try:
            vertex1 = self[name1]
        except KeyError:
            # create new vertex
            vertex1 = Vertex(name1)
            self[name1] = vertex1
        try:
            vertex2 = self[name2]
        except KeyError:
            # create new vertex
            vertex2 = Vertex(name2)
            self[name2] = vertex2
        vertex1.outgoing.append(vertex2)
        vertex2.incoming.append(vertex1)

    def __getitem__(self, vertex_name):
        """
        Get vertex object by name
        """
        return self.vertices[vertex_name]

    def __setitem__(self, key, value):
        """
        Set vertex object by name
        """
        if isinstance(value, Vertex):
            self.vertices[key] = value
        else:
            raise ValueError(u'Item must be a Vertex object')

    def __iter__(self):
        return self.vertices.itervalues()

    def __reversed__(self):
        return reversed(self.vertices)

    def __str__(self):
        return str(self.vertices)


class EdgeWeightedGraph(Graph):

    def add_edge(self, name1, name2, weight):
        try:
            vertex1 = self[name1]
        except KeyError:
            # create new vertex
            vertex1 = Vertex(name1)
            self[name1] = vertex1
        try:
            vertex2 = self[name2]
        except KeyError:
            # create new vertex
            vertex2 = Vertex(name2)
            self[name2] = vertex2
        vertex1.outgoing.append((vertex2, weight))
        vertex2.incoming.append((vertex1, weight))