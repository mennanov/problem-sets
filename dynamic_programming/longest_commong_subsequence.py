# -*- coding: utf-8 -*-
"""
The longest common subsequence of the strings "ABAC", "BAAC" is string "BAC" of length 3.
So it is not necessarily consecutive.
"""
from graph_shortest_path import memoize


class Substring(str):
    def __cmp__(self, other):
        if len(self) > len(other):
            return 1
        elif len(self) < len(other):
            return -1
        else:
            return 0


@memoize
def longest_subsequence(string1, string2, i=None, j=None):
    """
    Longest substring problem dynamic programming approach.
    The running time is O(mn)
    """
    if i is None:
        i = len(string1) - 1
    if j is None:
        j = len(string2) - 1
    if i < 0 or j < 0:
        # empty substring for empty strings
        return Substring()
    if string1[i] == string2[j]:
        return longest_subsequence(string1, string2, i - 1, j - 1) + string1[i]
    else:
        return max(longest_subsequence(string1, string2, i - 1, j), longest_subsequence(string1, string2, i, j - 1))
    return


if __name__ == '__main__':
    assert longest_subsequence('ABAC', 'BAAC') == 'BAC'