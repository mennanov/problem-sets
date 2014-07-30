# -*- coding: utf-8 -*-

"""
Goal: Find the substring containing only k unique characters that has maximum length.
For example for the string "ABBCA" and k=2 it can be "ABB" or "BBC"
"""
from graph_shortest_path import memoize


class Substring(object):
    def __init__(self, value=''):
        self.value = value
        self.chars = set(value)
        # mutability flag: helps to build a substring, not a subsequence
        self.mutable = True
        self.length = len(self.value)

    def append(self, char, limit):
        if self.mutable:
            if char in self.chars or len(self.chars) + 1 <= limit:
                self.value += char
                self.length += 1
                self.chars.add(char)
            else:
                self.mutable = False

    def prepend(self, char, limit):
        if self.mutable:
            if char in self.chars or len(self.chars) + 1 <= limit:
                self.value = char + self.value
                self.length += 1
                self.chars.add(char)
            else:
                self.mutable = False

    def __contains__(self, item):
        return item in self.chars

    def __len__(self):
        return self.length

    def __cmp__(self, other):
        if len(self) > len(other):
            return 1
        elif len(self) < len(other):
            return -1
        else:
            return 0

    def __str__(self):
        return str(self.value)

    def copy(self):
        c = type(self)(self.value[:])
        c.chars = self.chars
        c.mutable = self.mutable
        return c


class LongestUniqueSubstring(object):
    """
    Dynamic programming approach.
    Running time and space is O(N^2) (not sure about it though).
    This algorithm can be used for any value of k.
    Also it can be easily modified to return a subsequence (not a substring): just
    remove the "mutability" feature in a Substring class.
    """

    def __init__(self, string, limit):
        self.string = string
        self.limit = limit

    @memoize
    def run(self, i=0, j=None):
        if j is None:
            j = len(self.string) - 1
        if i == j:
            return Substring(self.string[i])
        if j < i:
            return Substring()

        case1 = self.run(i, j - 1).copy()
        case1.append(self.string[j], self.limit)

        case2 = self.run(i + 1, j).copy()
        case2.prepend(self.string[i], self.limit)

        case3 = self.run(i + 1, j - 1).copy()
        case3.append(self.string[j], self.limit)
        case3.prepend(self.string[i], self.limit)
        return max(case1, case2, case3)


def lsotuc(string):
    """
    Longest substring of two unique characters.
    It uses iterative approach and runs in O(N) with O(1) space.
    """
    # length, first char, last char
    longest_substring = (0, 0, 0)
    # pointer to the first occurrence of the first string
    a_first = 0
    # pointer to the second unique (not necessary last) occurrence of the first string
    a_second = 0
    # pointer to the first occurrence of the second string
    b_first = None
    # pointer to the second unique (not necessary last) occurrence of the second string
    b_second = None
    # change pointers flags
    change_a = False
    change_b = False
    for i in xrange(1, len(string)):
        if string[i] == string[a_first]:
            if change_a:
                a_second = i
                change_b = True
                change_a = False
        elif b_first is None:
            b_first = i
            b_second = i
            change_a = True
        elif string[i] == string[b_first]:
            if change_b:
                b_second = i
                change_a = True
                change_b = False
        else:
            start = min(a_first, b_first)
            end = i
            length = end - start
            if length > longest_substring[0]:
                # update the longest substring
                longest_substring = (length, start, end)

            # third character found
            if a_second > b_second:
                a_first = a_second
                b_first = b_second = i
                change_a = True
                change_b = False
            else:
                b_first = b_second
                a_first = a_second = i
                change_b = True
                change_a = False

    # check for the longest substring at the end of the cycle
    start = min(a_first, b_first)
    end = i + 1
    length = end - start
    if length > longest_substring[0]:
        # update the longest substring
        longest_substring = (length, start, end)

    return string[longest_substring[1]:longest_substring[2]]


if __name__ == '__main__':
    # it will hit the max recursion limit on input length > 330
    s = 'G4W1HTOYNY1KECQ8C4N3T3ASYS8E6YRFNJQ0Q63UMC96W7K2IJ2ZBV7Q3UIUA1PE3I9MLIZS8SLQFGWCG1PUKFTVZT3VF5EFEFUJ4VQD9IWBDBR3SBQKPJYLWL5EL7HGNBJJCB1RO0FE054OCMBR9GK9X7B2J4EIGYVQGXLO8QR43TQN3BK8HDVA07WIO8KZ02QR84EFHVE9W2W0KOGBCGA58OQLOJHGLHAV62JZ9R7KCH783J0OE943S2R50HY2H0QMZFQRXBFMW9VKWE19PDG660BK2Y4189Q9PH89NNRVEYBS3D3KRZ9KTXHO7QRBGL1TLWV0C3'
    lucs = LongestUniqueSubstring(s, 2)
    assert str(lucs.run()) == 'EFEF'
    assert lsotuc(s) == 'EFEF'