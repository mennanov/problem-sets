# -*- coding: utf-8 -*-
from random import randint


def random(items, lo, hi):
    """
    Choose a uniformly random integer within a given range(lo, hi) which is not
    presented in items (sorted list).
    """
    # number of integers which absent in items
    absent = hi - lo - len(items)
    # which absent number to pick
    pick = randint(0, absent - 1)
    # number of absent ints seen so far
    seen = 0

    def pick_absent(f, t):
        s = seen
        # iterate over absent ints
        for a in xrange(f, t):
            if pick == s:
                return a, s
            else:
                s += 1
        return None, s

    n = len(items)
    for i, num in enumerate(items):
        if i == 0:
            f, t = lo, items[i]
        elif 0 < i < n:
            f, t = items[i - 1] + 1, items[i]
        else:
            f, t = items[i] + 1, hi
        result, seen = pick_absent(f, t)
        if result is not None:
            return result


if __name__ == '__main__':
    print random([2, 3, 4, 7, 9, 18, 23], 0, 25)