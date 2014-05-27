# -*- coding: utf-8 -*-

compares = 0
calls = 0


def quicksort_compares(items, choose_pivot, lo=0, hi=None):
    """
    Finds the number of compares in quicksort algorithm
    with pivoting by the provided item.
    Number of compares are different with different pivots.
    This algorithm does not handle duplicate items (we should use 3-way partitioning instead).
    """
    global calls, compares
    calls += 1
    hi = hi if hi is not None else len(items) - 1
    if lo < hi:
        # choose pivot
        pivot = choose_pivot(items, lo, hi)
        items[lo], items[pivot] = items[pivot], items[lo]
        i = lo + 1
        # we will compare all the items in the given sub array except the pivot
        compares += hi - lo
        for j in xrange(i, hi + 1):
            if items[j] < items[lo]:
                items[i], items[j] = items[j], items[i]
                i += 1
        # put the pivot into the proper place
        items[lo], items[i - 1] = items[i - 1], items[lo]
        # left sub array
        quicksort_compares(items, choose_pivot, lo, i - 2)
        # right sub array
        quicksort_compares(items, choose_pivot, i, hi)
    else:
        # recursion tail: 0 compares
        return


def choose_median(items, lo, hi):
    mid = lo + (hi - lo) / 2
    return sorted([(items[lo], lo), (items[mid], mid), (items[hi], hi)], key=lambda x: x[0])[1][1]


if __name__ == '__main__':
    s = [3, 9, 8, 4, 6, 10, 2, 5, 7, 1]
    quicksort_compares(s[:], lambda i, l, h: l)
    assert compares == 25

    compares = 0
    quicksort_compares(s[:], lambda i, l, h: h)
    assert compares == 29

    compares = 0
    quicksort_compares(s[:], choose_median)
    assert compares == 21