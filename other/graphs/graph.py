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


class Edge(object):
    """
    Graph edge with 2 vertices
    """

    def __init__(self, vertex_from, vertex_to):
        self.vertex_from = vertex_from
        self.vertex_to = vertex_to

    def __repr__(self):
        return 'Edge({}, {})'.format(repr(self.vertex_from), repr(self.vertex_to))


class EdgeWeighted(object):
    """
    Graph weighted edge with 2 vertices and weight
    """

    def __init__(self, vertex_from, vertex_to, weight):
        self.vertex_from = vertex_from
        self.vertex_to = vertex_to
        self.weight = weight

    def __cmp__(self, other):
        if self.weight > other.weight:
            return 1
        elif self.weight < other.weight:
            return -1
        else:
            return 0

    def __repr__(self):
        return 'Edge({}, {}, {})'.format(repr(self.vertex_from), repr(self.vertex_to), repr(self.weight))


class Graph(object):
    """
    Directed graph API
    """
    def __init__(self, vertex_class=Vertex):
        self.vertices = OrderedDict()
        self.edges = []
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
        edge = Edge(vertex1, vertex2)
        vertex1.outgoing.append(edge)
        vertex2.incoming.append(edge)
        self.edges.append(edge)

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

    def iteredges(self):
        return iter(self.edges)

    def __reversed__(self):
        return reversed(self.vertices)

    def __str__(self):
        return str(self.vertices)

    def __len__(self):
        return len(self.vertices)


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
        edge = EdgeWeighted(vertex1, vertex2, weight)
        vertex1.outgoing.append(edge)
        vertex2.incoming.append(edge)
        self.edges.append(edge)