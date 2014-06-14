# -*- coding: utf-8 -*-
"""
K sum problem: in a given sequence of integers find k of them which sum will be 0.
This is a generalized version of a 2-SUM and a 3-SUM problems.
"""


def _combinations(items, length):
    """
    Generate unique combinations of sets of the given length
    """
    if length > 0:
        for i in xrange(len(items)):
            for cs in _combinations(items[i + 1:], length - 1):
                yield set([items[i]]) | cs
    else:
        yield set()


def ksum_naive(seq, k):
    """
    Naive implementation: iterate over all k-length sequences in a sequence and find ones which sum is 0.
    It will run O(N^k).
    """
    for c in _combinations(seq, k):
        if sum(c) == 0:
            yield c


def ksum_fast(seq, k):
    """
    The best possible approach: use meet-in-the-middle paradigm.
    Find all the sums of k / 2 length and populate a dictionary with them.
    For each sum try to find the opposite one.
    The running time is O(N^(k / 2))
    """
    sums = dict()
    # generate sums for all k / 2 combinations
    for cs in _combinations(seq, k / 2):
        s = sum(cs)
        if s not in sums:
            sums[s] = [cs]
        else:
            sums[s].append(cs)
    # using set is crucial here: if we use a list we will wind up with a very long
    # running time
    result = set()
    # try to find the opposite sums
    for s in sums:
        if -s in sums:
            # opposite sum is found
            for s1 in sums[s]:
                for s2 in sums[-s]:
                    # we don't need variants with duplicates, so we store set of frozensets
                    # and so avoid duplicate sets of k-sums
                    u = frozenset(s1 | s2)
                    if len(u) == k and u not in result:
                        result.add(u)
    return result


if __name__ == '__main__':
    from random import shuffle

    seq = range(-100, 100, 2)

    shuffle(seq)
    s1 = list(ksum_naive(seq, 4))
    s2 = ksum_fast(seq, 4)
    assert len(s1) == len(s2)