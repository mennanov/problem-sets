# -*- coding: utf-8 -*-


def permutations_2k(items):
    """
    Generate 2-length permutations of a given sequence.
    """
    l = len(items)
    for i in xrange(l):
        for j in xrange(l):
            if i != j:
                yield items[i], items[j]


def permutations_3k(items):
    """
    Generate 3-length permutations of a given sequence.
    """
    l = len(items)
    for i in xrange(l):
        for j in xrange(l):
            for k in xrange(l):
                if i != j and i != k and j != k:
                    yield items[i], items[j], items[k]


def xpermutations(items, length, exclude=None):
    """
    Recursively generate permutations of a given length.
    """
    if exclude is None:
        exclude = set()
    if length == 0:
        yield ()
    else:
        for i in xrange(len(items)):
            if i not in exclude:
                for subpermutation in xpermutations(items, length - 1, exclude | {i}):
                    yield (items[i], ) + subpermutation


def permutations(items, length, exclude=None):
    """
    Return all permutations as a list
    """
    if exclude is None:
        exclude = set()
    result = []
    if length == 1:
        for i in xrange(len(items)):
            if i not in exclude:
                result.append((items[i],))
    else:
        for i in xrange(len(items)):
            if i not in exclude:
                for subcombination in permutations(items, length - 1, exclude | {i}):
                    result.append((items[i],) + subcombination)
    return result


if __name__ == '__main__':
    from math import factorial

    seq = range(1, 5)
    n = len(seq)
    k = 2
    assert len(list(permutations_2k(seq))) == factorial(n) / factorial(n - k)
    k = 3
    assert len(list(permutations_3k(seq))) == factorial(n) / factorial(n - k)
    assert len(list(xpermutations(seq, 3))) == len(list(permutations_3k(seq)))
    assert len(permutations(seq, 3)) == len(list(permutations_3k(seq)))