# -*- coding: utf-8 -*-

"""
Implement an algorithm to output only unique characters from a string in a preserved order.
"""


def ordered_unique_set(string):
    """
    Running time and space is O(N).
    """
    chars = set()
    for c in string:
        if c not in chars:
            yield c
            chars.add(c)


def ordered_unique_list(string):
    """
    Running time is O(N), space is O(R) where R is a length of an alphabet.
    """
    # assume we have an ASCII string
    chars = [0] * (65535 if isinstance(string, unicode) else 255)
    for i, char in enumerate(string):
        chars[ord(char)] += 1
        if chars[ord(char)] == 1:
            yield char


def ordered_unique_bit(string):
    """
    Running time is O(N), required space is 1 byte only for ASCII string and 2 bytes for a Unicode string.
    Space usage is optimized using a bit vector.
    """
    # bit vector
    chars = 0
    for i, char in enumerate(string):
        # check if we have already seen this char
        if chars & (1 << ord(char)) == 0:
            yield char
            chars |= (1 << ord(char))


if __name__ == '__main__':
    s = 'aabcdffagkfd'
    assert list(ordered_unique_set(s)) == ['a', 'b', 'c', 'd', 'f', 'g', 'k']
    assert list(ordered_unique_list(s)) == ['a', 'b', 'c', 'd', 'f', 'g', 'k']
    assert list(ordered_unique_bit(s)) == ['a', 'b', 'c', 'd', 'f', 'g', 'k']
