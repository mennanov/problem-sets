# -*- coding: utf-8 -*-

"""
Given two strings check whether one string is a permutation of the other (anagram).
"""
from collections import Counter


def anagram_sort(string1, string2):
    """
    Simple and straightforward solution: sort both strings and check them for equality.
    Running time is O(NLogN), space consumption depends on the sorting algorithm.
    """
    # it is obvious that the length of these strings must be the same
    if len(string1) != len(string2):
        return False
    return sorted(string1) == sorted(string2)


def anagram_counting(string1, string2):
    """
    Count the number of occurrences of each character in each string.
    If all the numbers are the same - it is an anagram.
    Running time is O(N), space O(R), R - length of the alphabet.
    """
    # it is obvious that the length of these strings must be the same
    if len(string1) != len(string2):
        return False
    return Counter(string1) == Counter(string2)


if __name__ == '__main__':
    s1 = 'race'
    s2 = 'care'
    assert anagram_sort(s1, s2)
    assert anagram_counting(s1, s2)