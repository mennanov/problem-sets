# -*- coding: utf-8 -*-


def binary_search(needed, haystack):
    """
    Performs a binary search in a haystack array which must be sorted.
    Running time is O(LogN)
    """
    # establish bounds where we are going to search
    lo = 0
    hi = len(haystack) - 1
    while lo <= hi:
        # divide the search area into half
        mid = lo + (hi - lo) / 2
        if needed < haystack[mid]:
            # go search to the left part
            hi = mid - 1
        elif needed > haystack[mid]:
            # go search to the right part
            lo = mid + 1
        else:
            # match found
            return mid
    # return -1 if nothing is found
    return -1


def binary_search_rec(needed, haystack, lo=0, hi=None):
    """
    Recursive binary search example
    """
    lo = lo if lo is not None else 0
    hi = hi if hi is not None else len(haystack) - 1
    mid = lo + (hi - lo) / 2
    if lo <= hi:
        if needed < haystack[mid]:
            # go left
            return binary_search_rec(needed, haystack, lo, mid - 1)
        elif needed > haystack[mid]:
            # go right
            return binary_search_rec(needed, haystack, mid + 1, hi)
        else:
            # match
            return mid
    else:
        # no match found
        return -1

if __name__ == '__main__':
    l = range(0, 100, 3)
    assert binary_search(42, l) == l.index(42)
    assert binary_search_rec(42, l) == l.index(42)