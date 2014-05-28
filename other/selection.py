# -*- coding: utf-8 -*-

"""
Selection problem is the problem when we need to find the i-th element in the
unsorted list so that if the list was sorted.
The problem can be easily reduced to sorting and then selecting any element you want.
But also it may be solved even faster with deterministic and non-deterministic algorithms below.
"""

from random import randint
from math import ceil


def select(items, needle, choose_pivot, lo=0, hi=None):
    """
    The running time of the algorithm strongly depends on how the pivot is chosen.
    The pivot may be chosen randomly or may be computed by the deterministic algorithm.
    See the 'choose_pivot' argument.
    Both methods are pretty fast, though the random pivoting works faster on average than
    the deterministic pivoting, but may run quadratic if we are not lucky with pivoting (extremely unlikely).
    While deterministic pivoting provides an upper bound linear time (so does the lower bound), though uses
    extra memory to perform pivot selection.
    """
    hi = hi if hi is not None else len(items) - 1
    if lo <= hi:
        # choose pivot
        pivot = choose_pivot(items, lo, hi)
        assert lo <= pivot <= hi
        # put the pivot at the first position to simplify partitioning
        items[lo], items[pivot] = items[pivot], items[lo]
        i = lo + 1
        for j in xrange(i, hi + 1):
            if items[j] < items[lo]:
                items[i], items[j] = items[j], items[i]
                i += 1
        # pivot new index
        pivot = i - 1
        # put the pivot into the proper place
        items[lo], items[pivot] = items[pivot], items[lo]
        if needle < pivot:
            # left sub array
            return select(items, needle, choose_pivot, lo, pivot - 1)
        elif needle > pivot:
            # right sub array
            return select(items, needle, choose_pivot, pivot + 1, hi)
        else:
            # recursion tail: match found
            return items[pivot]
    else:
        # recursion tail: match was not found
        raise KeyError(needle)


def random_pivot(items, lo, hi):
    """
    Randomly choose the pivot from 'lo' to 'hi'
    """
    return randint(lo, hi)


def median_of_medians(items, lo, hi):
    """
    The idea is to break the items into n/5 groups so each group will have
    5 elements at most.
    Then we need to find the median of each group and create a new list of these medians.
    Finding the median out of 5 elements can be done almost in constant time so we don't increase
    the overall running time of the algorithm here.
    """
    if lo < hi:
        bound_items = items[lo:hi + 1]
        # create groups of 5 elements each
        groups = [h for h in [bound_items[x:x + 5] for x in xrange(0, len(items), 5)] if h]
        # sort each group and find the median
        medians = []
        for group in groups:
            group.sort()
            medians.append(group[int(ceil(len(group) / 2))])
        # recursively compute the median of the medians
        pivot_value = select(medians, int(ceil(len(medians) / 2)), median_of_medians)
        # we need an index of the pivot in items list instead of its value
        return items.index(pivot_value)
    else:
        return lo


if __name__ == '__main__':
    from random import shuffle

    arr = range(0, 300, 3)
    shuffle(arr)
    # random pivoting
    assert select(arr[:], 5, random_pivot) == 15
    # deterministic pivoting
    assert select(arr[:], 5, median_of_medians) == 15
