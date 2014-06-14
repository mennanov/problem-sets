# -*- coding: utf-8 -*-
"""
Three sum problem: in a given sequence of integers find three of them which sum will be 0.
"""


def threesum_naive(seq):
    """
    Naive implementation: iterate over all triplets in a sequence and find ones which sum is 0.
    It will run O(N^3).
    """
    for i in xrange(len(seq)):
        for j in xrange(len(seq)):
            if seq[i] + seq[j] == 0:
                yield seq[i], seq[j]


def twosum_faster(seq):
    """
    A better approach: sort all the numbers and try to find the opposite number
    for each number with a binary search.
    It will take O(NlogN) for sorting and O(NLogN) for overall binary search look ups,
    so finally the running time is O(NLogN).
    """
    seq_srt = sorted(seq)

    def bs(items, needed, lo, hi):
        """
        Binary search
        """
        while lo <= hi:
            mid = lo + (hi - lo) / 2
            if needed < items[mid]:
                hi = mid - 1
            elif needed > items[mid]:
                lo = mid + 1
            else:
                return mid
        return None

    l = len(seq)
    for i in xrange(l):
        j = bs(seq_srt, -seq_srt[i], 0, l - 1)
        if j is not None:
            yield seq_srt[i], seq_srt[j]


def twosum_fastest(seq):
    """
    The best possible approach: populate a dictionary (or set) with every item.
    Then iterate over every item in the set and try to find the opposite one.
    This will run O(N).
    """
    s = set()
    for item in seq:
        s.add(item)
    for i in s:
        if -i in s:
            yield i, -i


if __name__ == '__main__':
    from random import shuffle

    seq = range(-100, 100, 8)
    shuffle(seq)
    assert len(list(twosum_naive(seq))) == 24
    assert len(list(twosum_faster(seq))) == 24
    assert len(list(twosum_fastest(seq))) == 24
