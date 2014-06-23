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
        # the list of items which were put in
        self.items = []

    def add(self, item):
        """
        Add item to the knapsack
        """
        self.items.append(item)
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
    Knapsack with repetitions dynamic programming algorithm.
    This algorithm allows infinite repetitions of items.
    It runs O(NW) with memoization and runs in exponential time without.
    """

    def __init__(self, items):
        self.items = items

    @memoize
    def knapsack(self, weight):
        """
        Return the best possible knapsack for the given weight
        """
        if weight <= 0:
            # empty knapsack for empty set of items
            return Knapsack()
        # add an empty knapsack by default
        # it will be used if no items are added at the next step
        knapsacks = [Knapsack()]
        for item in self.items:
            # filter items which still can be put into the knapsack
            if item.weight <= weight:
                knapsack = self.knapsack(weight - item.weight).copy()
                knapsack.add(item)
                knapsacks.append(knapsack)
        return max(knapsacks)


class RobberyBF(object):
    """
    Knapsack with repetitions brute force algorithm.
    It uses generation of multicombinations
    (http://en.wikipedia.org/wiki/Combination#Number_of_combinations_with_repetition)
    So the overall running time of the algorithm is: O(min(weight) * sum(1 .. weight/min(weight), choose(n, k)))
    which is nearly exponential and unbelievably slow, so, please, don't use it :)
    """

    def __init__(self, items):
        self.items = items

    def _multicombinations(self, items, length):
        """
        Generate combinations with repetitions
        """
        if length == 1:
            for item in items:
                yield (item,)
        else:
            for item in items:
                for subcombination in self._multicombinations(items, length - 1):
                    yield (item,) + subcombination

    def knapsack(self, weight):
        """
        Return the best possible knapsack for the given weight
        """
        # calculate max length of combinations: the worst case is when we use
        # only the item with the smallest weight
        max_length = weight / min(self.items).weight
        # keep the best combination so far
        best = Knapsack()
        for length in xrange(1, max_length + 1):
            # generate all possible multicombinations for a given length
            for combination in self._multicombinations(self.items, length):
                knapsack = Knapsack()
                for item in combination:
                    knapsack.add(item)
                if knapsack.weight <= weight and knapsack > best:
                    best = knapsack
        return best


if __name__ == '__main__':
    items = (Item(6, 30), Item(3, 14), Item(4, 16), Item(2, 9))
    robbery = RobberyDP(items)
    bag1 = robbery.knapsack(15)
    robbery = RobberyBF(items)
    bag2 = robbery.knapsack(15)
    assert all([i in bag2 for i in bag1]) and len(bag1) == len(bag2)