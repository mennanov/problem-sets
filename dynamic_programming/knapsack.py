# -*- coding: utf-8 -*-

"""
During a robbery, a burglar finds much more loot than he had expected and has to decide what to take.
His bag (or "knapsack") will hold a total weight of at most W pounds. There are n items to pick from.
Each item has its own weight and a dollar value.
What's the most valuable combination of items he can fit into his bag?
"""
import heapq
from collections import defaultdict
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

    def __add__(self, other):
        """
        Add two knapsacks together
        """
        assert len(self.items & other.items) == 0, 'Adding knapsacks with common items is not allowed'
        result = self.copy()
        for item in other:
            result.add(item)
        return result


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

    def _combinations(self, items, length, start=0):
        """
        Generate combinations without repetitions
        """
        if length == 1:
            for i in xrange(start, len(items)):
                yield (items[i],)
        else:
            for i in xrange(start, len(items)):
                for subcombination in self._combinations(items, length - 1, i + 1):
                    yield (items[i],) + subcombination

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


class RobberyMIM(object):
    """
    Knapsack without repetitions Meet-in-the-middle algorithm.
    The running time is O(n*2^(n/2)) which is faster than a brute force algorithm
    and even sometimes faster than a dynamic programming approach if W is much larger than N since
    the running time does not depend on W in this case.
    """

    def __init__(self, items):
        self.items = items

    def _combinations(self, items, lo, hi, length):
        """
        Generate combinations without repetitions
        """
        if length == 1:
            for i in xrange(lo, hi):
                yield (items[i],)
        else:
            for i in xrange(lo, hi):
                for subcombination in self._combinations(items, i + 1, hi, length - 1):
                    yield (items[i],) + subcombination

    def knapsack(self, weight):
        """
        Return the best possible knapsack for the given weight
        """
        # divide the items into two parts
        n = len(self.items)
        # all possible knapsacks with the items from the left subset
        l_knapsacks = []
        # generate combinations for the left part
        for length in xrange(1, n / 2 + 1):
            # generate all possible combinations for a given length
            for combination in self._combinations(self.items, 0, n / 2, length):
                knapsack = Knapsack()
                for item in combination:
                    knapsack.add(item)
                # if knapsack is not over-weighted
                if knapsack.weight <= weight:
                    l_knapsacks.append(knapsack)
        # store all the possible knapsacks for the right subset grouped by weight
        # maintaining max-oriented heap with knapsacks
        r_knapsacks = defaultdict(list)
        # generate combinations for the right part
        for length in xrange(1, n / 2 + 1):
            # generate all possible combinations for a given length
            for combination in self._combinations(self.items, n / 2, n, length):
                knapsack = Knapsack()
                for item in combination:
                    knapsack.add(item)
                # if knapsack is not over-weighted
                if knapsack.weight <= weight:
                    heapq.heappush(r_knapsacks[knapsack.weight], (-knapsack.value, knapsack))
        # keep the best combined knapsack so far
        best = Knapsack()
        # for every knapsack in the left subset try to find the best possible
        # knapsack in the right subset such as their combination is not over-weighted
        for left in l_knapsacks:
            right_weight = weight - left.weight
            right = Knapsack()
            while right_weight > 0:
                    right_heap = r_knapsacks[right_weight]
                    # get the most valuable knapsack of the given weight
                    if len(right_heap) > 0:
                        right = right_heap[0][1]
                        break
                    else:
                        # the perfect weighted knapsack was not found: decrease the weight and search again
                        right_weight -= 1
            # combine left and right knapsacks
            combined = left + right
            if combined > best:
                best = combined
        return best


if __name__ == '__main__':
    items = (Item(6, 30), Item(3, 14), Item(4, 16), Item(2, 9))
    robbery = RobberyDP(items)
    bag1 = robbery.knapsack(10)
    robbery = RobberyBF(items)
    bag2 = robbery.knapsack(10)
    assert all([i in bag2 for i in bag1]) and len(bag1) == len(bag2)
    robbery = RobberyMIM(items)
    bag3 = robbery.knapsack(10)
    assert all([i in bag3 for i in bag2]) and len(bag2) == len(bag3)