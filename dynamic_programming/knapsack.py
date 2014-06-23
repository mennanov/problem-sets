# -*- coding: utf-8 -*-

"""
During a robbery, a burglar finds much more loot than he had expected and has to decide what to take.
His bag (or "knapsack") will hold a total weight of at most W pounds. There are n items to pick from.
Each item has its own weight and a dollar value.
What's the most valuable combination of items he can fit into his bag?
"""
from graph_shortest_path import memoize


class Item(object):
    """
    Item which can be put in a knapsack
    """

    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

    def __str__(self):
        return '{} pounds, ${}'.format(str(self.weight), str(self.value))

    def __repr__(self):
        return 'Item({}, {})'.format(repr(self.weight), repr(self.value))

    def __cmp__(self, other):
        """
        Compare by weight
        """
        if self.weight < other.weight:
            return -1
        elif self.weight > other.weight:
            return 1
        else:
            return 0


class Knapsack(object):
    """
    Knapsack with items
    """

    def __init__(self):
        # total weight
        self.weight = 0
        # total dollar value
        self.value = 0
        # the set of items which were put in
        self.items = set()

    def add(self, item):
        """
        Add item to the knapsack
        """
        self.items.add(item)
        self.value += item.value
        self.weight += item.weight

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return '{}, {} pounds, ${}'.format(str(self.items), str(self.weight), str(self.value))

    def __cmp__(self, other):
        """
        Compare by value
        """
        if self.value < other.value:
            return -1
        elif self.value > other.value:
            return 1
        else:
            return 0

    def copy(self):
        """
        Create a copy of the object
        """
        c = Knapsack()
        for item in self.items:
            c.add(item)
        return c


class RobberyDP(object):
    """
    Knapsack without repetitions dynamic programming algorithm.
    This algorithm does not allow repetitions of items.
    It runs O(NW) with memoization and runs in exponential time without.
    """

    def __init__(self, items):
        self.items = items

    @memoize
    def knapsack(self, weight, used=None):
        """
        Return the best possible knapsack for the given weight
        """
        if weight <= 0:
            # empty knapsack for empty set of items
            return Knapsack()
        if used is None:
            # set of already used items
            used = frozenset()
        # add an empty knapsack by default
        # it will be used if no items are added at the next step
        knapsacks = [Knapsack()]
        for item in self.items:
            # filter items which still can be put into the knapsack
            if item.weight <= weight and item not in used:
                knapsack = self.knapsack(weight - item.weight, used | frozenset([item])).copy()
                knapsack.add(item)
                knapsacks.append(knapsack)
        return max(knapsacks)


class RobberyBF(object):
    """
    Knapsack without repetitions brute force algorithm.
    It uses generation of combinations
    (http://en.wikipedia.org/wiki/Combination)
    So the overall running time of the algorithm is: O(N!)
    which is very slow and can not be used in practice.
    """

    def __init__(self, items):
        self.items = items

    def _combinations(self, items, length, used=None):
        """
        Generate combinations without repetitions
        """
        if used is None:
            used = set()
        if length == 1:
            for item in items:
                if item not in used:
                    yield (item,)
        else:
            for item in items:
                if item not in used:
                    for subcombination in self._combinations(items, length - 1, used | {item}):
                        yield (item,) + subcombination

    def knapsack(self, weight):
        """
        Return the best possible knapsack for the given weight
        """
        # keep the best combination so far
        best = Knapsack()
        # generate combinations with length 1 to n
        for length in xrange(1, len(self.items) + 1):
            # generate all possible combinations for a given length
            for combination in self._combinations(self.items, length):
                knapsack = Knapsack()
                for item in combination:
                    knapsack.add(item)
                if knapsack.weight <= weight and knapsack > best:
                    best = knapsack
        return best


if __name__ == '__main__':
    items = (Item(6, 30), Item(3, 14), Item(4, 16), Item(2, 9))
    robbery = RobberyDP(items)
    bag1 = robbery.knapsack(10)
    robbery = RobberyBF(items)
    bag2 = robbery.knapsack(10)
    assert all([i in bag2 for i in bag1]) and len(bag1) == len(bag2)