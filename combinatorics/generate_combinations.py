# -*- coding: utf-8 -*-
from math import factorial


def combinations_2k(items):
    """
    Generate 2-length combinations of a given sequence.
    """
    l = len(items)
    for i in xrange(l - 1):
        for j in xrange(i + 1, l):
            yield items[i], items[j]


def combinations_3k(items):
    """
    Generate 3-length combinations of a given sequence.
    """
    l = len(items)
    for i in xrange(l - 2):
        for j in xrange(i + 1, l - 1):
            for k in xrange(j + 1, l):
                yield items[i], items[j], items[k]


def xcombinations(items, length, start=0):
    """
    Recursively generate combinations of a given length.
    """
    if length == 0:
        yield ()
    else:
        for i in xrange(start, len(items) - length + 1):
            for subcombination in xcombinations(items, length - 1, i + 1):
                yield (items[i], ) + subcombination


def combinations(items, length, start=0):
    """
    Return all combinations as a list
    """
    result = []
    if length == 1:
        for i in xrange(start, len(items)):
            result.append((items[i],))
    else:
        for i in xrange(start, len(items) - length + 1):
            for subcombination in combinations(items, length - 1, i + 1):
                result.append((items[i],) + subcombination)
    return result


if __name__ == '__main__':
    seq = range(1, 5)
    n = len(seq)
    k = 2
    assert len(list(combinations_2k(seq))) == factorial(n) / (factorial(k) * factorial(n - k))
    k = 3
    assert len(list(combinations_3k(seq))) == factorial(n) / (factorial(k) * factorial(n - k))
    assert len(list(xcombinations(seq, 3))) == len(list(combinations_3k(seq)))
    assert len(combinations(seq, 3)) == len(list(combinations_3k(seq)))