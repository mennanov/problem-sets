# -*- coding: utf-8 -*-

"""
Graph API
"""
from collections import OrderedDict


class SimpleVertex(object):
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


class Vertex(SimpleVertex):

    def __init__(self, *args):
        super(Vertex, self).__init__(*args)
        # set the distance to infinity by default
        self.distance = float('inf')
        # what vertex can we get to that one from
        self.prev = None

    def __cmp__(self, other):
        if self.distance > other.distance:
            return 1
        elif self.distance < other.distance:
            return -1
        else:
            return 0


class Graph(object):
    """
    Directed graph API
    """
    def __init__(self, vertex_class=SimpleVertex):
        self.vertices = OrderedDict()
        self.vertex_class = vertex_class

    def add_edge(self, name1, name2):
        try:
            vertex1 = self[name1]
        except KeyError:
            # create new vertex
            vertex1 = self.vertex_class(name1)
            self[name1] = vertex1
        try:
            vertex2 = self[name2]
        except KeyError:
            # create new vertex
            vertex2 = self.vertex_class(name2)
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
        if isinstance(value, self.vertex_class):
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
            vertex1 = self.vertex_class(name1)
            self[name1] = vertex1
        try:
            vertex2 = self[name2]
        except KeyError:
            # create new vertex
            vertex2 = self.vertex_class(name2)
            self[name2] = vertex2
        vertex1.outgoing.append((vertex2, int(weight)))
        vertex2.incoming.append((vertex1, int(weight)))