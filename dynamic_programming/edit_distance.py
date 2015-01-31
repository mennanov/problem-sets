# -*- coding: utf-8 -*-
from graph_shortest_path import memoize


class Case(object):
    """
    Subproblem class which stores the editing distance and additional information
    to build up the final answer
    """

    def __init__(self, top=None, bottom=None):
        self.first = top
        self.second = bottom
        # next step
        self.next = None
        # current edit distance
        self.distance = 0

    def __cmp__(self, other):
        if self.distance > other.distance:
            return 1
        elif self.distance < other.distance:
            return -1
        else:
            return 0

    def copy(self):
        cp = Case(self.first, self.second)
        cp.distance = self.distance
        cp.next = self.next.copy() if self.next is not None else None
        return cp

    def __str__(self):
        return '{} {} ({})'.format(str(self.first), str(self.second), str(self.distance))


class EditDistance(object):
    """
    This is a famous Levenshtein edit distance algorithm.
    We need to calculate edit distance between two strings with the following operations:
    delete a symbol, insert a symbol and swap two symbols in order to get the second string from the first one.

    """

    def __init__(self, first=None, second=None):
        self.first = first
        self.second = second
        self.strategy = self._distance(len(self.first) - 1, len(self.second) - 1)

    @memoize
    def _distance(self, i, j):
        if i == -1 and j >= 0:
            case = Case('-' * (j + 1), self.second[:j + 1])
            case.distance = j + 1
            return case
        elif j == -1 and i >= 0:
            case = Case(self.first[:i + 1], '-' * (i + 1))
            case.distance = i + 1
            return case
        elif i == j == -1:
            return Case()

        # step 1: use the top letter and put a gap to the bottom
        case1 = Case(self.first[i], '-')
        case1.next = self._distance(i - 1, j).copy()
        # it takes 1 edit distance
        case1.distance = case1.next.distance + 1
        # step 2: use the bottom letter and put a gap to the top
        case2 = Case('-', self.second[j])
        case2.next = self._distance(i, j - 1).copy()
        # it takes 1 edit distance
        case2.distance = case2.next.distance + 1
        # step 3: use both letters
        case3 = Case(self.first[i], self.second[j])
        case3.next = self._distance(i - 1, j - 1).copy()
        # it takes either 0 or 1 edit distance
        case3.distance = case3.next.distance + int(self.first[i] != self.second[j])
        # choose the best step from these three
        return min(case1, case2, case3)

    def distance(self):
        return self.strategy.distance

    def visualize(self):
        case = self.strategy
        first = ''
        second = ''
        while case is not None:
            first += case.first[::-1]
            second += case.second[::-1]
            case = case.next
        return '{}\n{}'.format(first[::-1], second[::-1])

if __name__ == '__main__':
    ed = EditDistance('exponential', 'polynomial')
    assert ed.distance() == 6
    assert ed.visualize() == 'exponent-ial\n--polynomial'

