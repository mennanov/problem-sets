# -*- coding: utf-8 -*-


"""
A subsequence is palindromic if it is the same whether read left to right or right to left. For
instance, the sequence
A, C, G, T, G, T, C, A, A, A, A, T, C, G
has many palindromic subsequences, including A, C, G, C, A and A, A, A, A (on the other hand,
the subsequence A, C, T is not palindromic).
Goal: compute the longest palindromic subsequence.
"""

from graph_shortest_path import memoize


class Palindrome(object):
    """
    Palindrome object
    """

    def __init__(self, middle=None):
        self.left = []
        self.middle = middle
        self.right = []

    def __len__(self):
        return len(self.left) + len(self.right)

    def __cmp__(self, other):
        if len(self) > len(other):
            return 1
        elif len(self) < len(other):
            return -1
        else:
            return 0

    def __str__(self):
        return str(self.left[::-1] + [self.middle] + self.right if self.middle else self.left[::-1] + self.right)

    def copy(self):
        c = self.__class__()
        c.left = self.left[:]
        c.middle = self.middle
        c.right = self.right[:]
        return c


class PalindromicSubsequence(object):
    """
    Longest palindromic subsequence: dynamic programming approach.
    Running time is O(N^2)
    """

    def __init__(self, iterable):
        self.iterable = iterable

    @memoize
    def run(self, lo=None, hi=None):
        if lo is None:
            lo = 0
        if hi is None:
            hi = len(self.iterable) - 1

        if lo == hi:
            # 1 letter is also a palindrome
            return Palindrome(self.iterable[lo])
        elif lo > hi:
            # empty palindrome
            return Palindrome()

        if self.iterable[lo] == self.iterable[hi]:
            # first and last letters are equal - find a palindrome between these boundaries
            p = self.run(lo + 1, hi - 1).copy()
            # wrap the palindrome with the current letters
            p.left.append(self.iterable[lo])
            p.right.append(self.iterable[hi])
            return p
        else:
            return max(self.run(lo + 1, hi), self.run(lo, hi - 1))


if __name__ == '__main__':
    sequence = 'A, C, G, T, G, T, C, A, A, A, A, T, C, G'.split(', ')
    pl = PalindromicSubsequence(sequence)
    assert pl.run() == ['G', 'C', 'A', 'A', 'A', 'A', 'C', 'G']
