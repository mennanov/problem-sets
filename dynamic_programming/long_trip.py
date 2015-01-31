# -*- coding: utf-8 -*-

"""
You are going on a long trip. You start on the road at mile post 0. Along the way there are n
hotels, at mile posts a1 < a2 < · · · < an, where each ai is measured from the starting point. The
only places you are allowed to stop are at these hotels, but you can choose which of the hotels
you stop at. You must stop at the ﬁnal hotel (at distance an), which is your destination.
You’d ideally like to travel 200 miles a day, but this may not be possible (depending on the spacing
of the hotels). If you travel x miles during a day, the penalty for that day is (200 − x)^2
You want to plan your trip so as to minimize the total penalty—that is, the sum, over all travel days, of the
daily penalties.
Goal: determine the optimal sequence of hotels at which to stop.
"""

from graph_shortest_path import memoize


class Route(object):
    """
    Route with hotels and total penalty
    """

    def __init__(self, penalty=0):
        self.hotels = []
        self.penalty = penalty

    def __cmp__(self, other):
        if self.penalty > other.penalty:
            return 1
        elif self.penalty < other.penalty:
            return -1
        else:
            return 0

    def visit_hotel(self, hotel, penalty):
        self.hotels.append(hotel)
        self.penalty += penalty

    def copy(self):
        c = Route()
        c.hotels = self.hotels[:]
        c.penalty = self.penalty
        return c

    def __str__(self):
        return 'Hotels: {}, penalty: {}'.format(str(self.hotels), str(self.penalty))


class LongTripDP(object):
    """
    Long trip dynamic programming approach.
    For each hotel we find the route with the lowest penalty.
    Running time is O(n^2).
    """

    def __init__(self, distances, penalty):
        self.penalty = penalty
        self.distances = distances

    @memoize
    def travel(self, position=None):
        if position is None:
            position = len(self.distances) - 1
        if position == -1:
            return Route()
        best_route = Route(float('inf'))
        for i in xrange(position - 1, -2, -1):
            route = self.travel(i).copy()
            diff = self.distances[position] - self.distances[i] if i >= 0 else self.distances[position]
            route.visit_hotel(position, self.penalty(diff))
            if route < best_route:
                best_route = route
        return best_route


if __name__ == '__main__':
    distances = [150, 200, 320, 380, 420, 600]
    trip = LongTripDP(distances, lambda x: (200 - x) ** 2)
    assert trip.travel().hotels == [1, 4, 5]