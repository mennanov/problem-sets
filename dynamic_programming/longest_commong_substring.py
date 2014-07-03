# -*- coding: utf-8 -*-
"""
The longest common substring of the strings "ABABC", "BABCA" and "ABCBA" is string "ABC" of length 3.
Other common substrings are "AB", "BC" and "BA".
"""


def longest_substring(string1, string2):
    """
    Longest substring problem dynamic programming approach.
    The running time is O(mn).
    Bottom-up version with no recursion.
    """
    # TODO: return substring instead of the length
    table = []
    for c in xrange(len(string1)):
        table.append([0] * (len(string2)))
    # the longest table substring indexes
    u, v = 0, 0
    for i in xrange(len(string1)):
        for j in xrange(len(string2)):
            if string1[i] == string2[j]:
                # strings match
                if i > 0 and j > 0:
                    table[i][j] = table[i - 1][j - 1] + 1
                else:
                    table[i][j] = 1
                if table[i][j] > table[u][v]:
                    # update the longest substring indexes so far
                    u = i
                    v = j
    return table[u][v]


if __name__ == '__main__':
    assert longest_substring('ABABC', 'BABCA') == 4