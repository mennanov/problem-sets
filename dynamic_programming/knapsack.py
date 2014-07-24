# -*- coding: utf-8 -*-

"""
During a robbery, a burglar finds much more loot than he had expected and has to decide what to take.
His bag (or "knapsack") will hold a total weight of at most W pounds. There are n items to pick from.
Each item has its own weight and a dollar value.
What's the most valuable combination of items he can fit into his bag?
Different approaches are analysed and compared here: http://micsymposium.org/mics_2005/papers/paper102.pdf
"""
import heapq
from collections import defaultdict
from graph_shortest_path import memoize
from combinatorics.generate_combinations import xcombinations_gray


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
            # if weight is the same - give the most valuable item
            return cmp(self.value, other.value)


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
        for i, item in enumerate(self.items):
            # filter items which still can be put into the knapsack
            if item.weight <= weight and i not in used:
                knapsack = self.knapsack(weight - item.weight, used | frozenset([i])).copy()
                knapsack.add(item)
                knapsacks.append(knapsack)
        return max(knapsacks)


class RobberyBF(object):
    """
    Knapsack without repetitions brute force algorithm.
    It uses generation of 2^n combinations using a generator which must be provided
    So the overall running time of the algorithm is: O(N*2^N)
    which is very slow and can not be used in practice.
    """

    def __init__(self, items):
        self.items = items

    def knapsack(self, weight, combinations_generator):
        """
        Return the best possible knapsack for the given weight
        """
        # keep the best combination so far
        best = Knapsack()
        # iterate over all possible 2^N combinations
        for combination in combinations_generator(self.items):
            knapsack = Knapsack()
            for item in combination:
                knapsack.add(item)
            if knapsack.weight <= weight and knapsack > best:
                best = knapsack
        return best


class RobberyBB(object):
    """
    Knapsack without repetitions branch-and-bound algorithm.
    It is an improvement over brute force search, because unlike it, branch and bound constructs
    candidate solutions one component at a time and evaluates the partly constructed
    solutions. If no potential values of the remaining components can lead to a solution, the
    remaining components are not generated at all. This approach makes it possible to solve
    some large instances of difficult combinatorial problems, though, in the worst case, it still
    has an exponential complexity.
    Overall running time of the algorithm in the worst case is still O(N*2^N)
    but it surely beats brute-force approach and even sometimes dynamic programming approach when
    the number of items is not huge.
    """

    def __init__(self, items):
        self.items = items

    def _combinations(self, items, constraint, partial_weight=0, prefix=(), start=0):
        """
        Generate combinations using prefixes which satisfy a given constraint
        """
        for i in xrange(start, len(items)):
            item = items[i]
            # use this combination if it satisfies a constraint
            if partial_weight + item.weight <= constraint:
                combination = prefix + (item,)
                yield combination
                if partial_weight + item.weight < constraint:
                    for c in self._combinations(items, constraint, partial_weight + item.weight, combination, i + 1):
                        yield c

    def knapsack(self, weight):
        """
        Return the best possible knapsack for the given weight
        """
        # keep the best combination so far
        best = Knapsack()
        # iterate over all possible successful combinations (at most 2^N)
        for combination in self._combinations(self.items, weight):
            knapsack = Knapsack()
            for item in combination:
                knapsack.add(item)
            if knapsack > best:
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

    def knapsack(self, weight, combinations_generator):
        """
        Return the best possible knapsack for the given weight
        """
        # divide the items into two parts
        n = len(self.items)
        # all possible knapsacks with the items from the left subset
        l_knapsacks = []
        # generate combinations for the left part
        for combination in combinations_generator(self.items[:n / 2]):
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
        # generate all possible combinations for a given length
        for combination in combinations_generator(self.items[n / 2:]):
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


def knapsack_memo(items, weight):
    """
    Memory efficient solution: it takes only O(W) space and returns the max value of the knapsack,
    but does not track the set of items in the knapsack.
    The running time is still O(nW).
    We may improve this algorithm further by sorting the items in the weight decreasing order and stop
    iteration when is does not make sense. But this condition is intricate.
    """
    # we don't use a dictionary here since it may cause a MemoryError on a huge input
    table = [0] * (weight + 1)
    for i, item in enumerate(items):
        for w in xrange(weight, item.weight - 1, -1):
            if item.weight <= w:
                table[w] = max(table[w], table[w - item.weight] + item.value)

    return table[weight]


if __name__ == '__main__':
    items = (Item(6, 30), Item(3, 14), Item(4, 16), Item(2, 9))
    robbery = RobberyDP(items)
    bag1 = robbery.knapsack(10)
    robbery = RobberyBF(items)
    bag2 = robbery.knapsack(10, xcombinations_gray)
    assert all([i in bag2 for i in bag1]) and len(bag1) == len(bag2)
    robbery = RobberyMIM(items)
    bag3 = robbery.knapsack(10, xcombinations_gray)
    assert all([i in bag3 for i in bag2]) and len(bag2) == len(bag3)
    robbery = RobberyBB(items)
    bag4 = robbery.knapsack(10)
    assert all([i in bag4 for i in bag3]) and len(bag3) == len(bag4)
    assert knapsack_memo(items, 10) == 46
