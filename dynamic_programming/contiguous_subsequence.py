# -*- coding: utf-8 -*-

"""
A contiguous subsequence of a list S is a subsequence made up of consecutive elements of S. For
instance, if S is
5, 15, -30, 10, -5, 40, 10,
then 15, −30, 10 is a contiguous subsequence but 5, 15, 40 is not.
Goal: find the contiguous subsequence of a maximum sum.
"""
from graph_shortest_path import memoize


class ContiguousSubsequenceDP(object):
    """
    A contiguous subsequence dynamic programming approach.
    Running time is O(n), space required is also O(n).
    """

    def __init__(self, iterable):
        self.iterable = iterable
        # left boundary
        self.i = 0
        # right boundary
        self.j = 0
        # result sum
        self.result = None

    def run(self):
        if self.result is None:
            self.result = self._max_sub()
        return self.iterable[self.i:self.j + 1]

    @memoize
    def _max_sub(self, position=None):
        if position is None:
            position = len(self.iterable) - 1
        elif position == 0:
            # recursion tail
            return self.iterable[0]
        gain = self._max_sub(position - 1) + self.iterable[position]
        reset = self.iterable[position]
        if gain > reset:
            self.j = position
            return gain
        else:
            # reset the sum to the current item since it is better than the whole preceding subsequence
            self.i = position
            return reset


if __name__ == '__main__':
    sequence = [5, 15, -30, 10, -5, 40, 10]
    csdp = ContiguousSubsequenceDP(sequence)
    assert csdp.run() == [10, -5, 40, 10]
