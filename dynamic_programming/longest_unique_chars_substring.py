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
    Apparently O(N) space and time.
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


if __name__ == '__main__':
    s = 'JBEEVRVCFYHRKMRFPZWTBKBEAFPNDNMPFDPEJGWMOUBOMRDZHOHMOSJZHJOTZSHLOBXAQKCYKNNBCVMLXFOMABEZJHCOWHNRQZYVZKPRBKQNAMYBRGARTXAJMORWERIGLCNYXNXOMKYJKUFBTKTLOFQIZXYPKUFPGWBWWKANXSWTHUXIBGOSAJXPWHNLNZAXAZTQVKVISNKTYWECFOYBCIUMOQDAMHHOWVXBZWARUQCRGLOCGEJPGFFMGPDYQLIPDNOJBNFOYDJUVXHBJQHAAJBDYMUULIWZLWIHYMQEHODAJRPJLCTJMJVOIOFGCMBCVHGSGLZDYD'
    lucs = LongestUniqueSubstring(s, 5)
    assert str(lucs.run()) == 'FPNDNMPFDP'