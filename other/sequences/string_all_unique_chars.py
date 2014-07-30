# -*- coding: utf-8 -*-

"""
Implement an algorithm to determine if a string has all unique characters.
"""


def all_unique_set(string):
    """
    Running time and space is O(N).
    """
    return len(string) == len(set(string))


def all_unique_list(string):
    """
    Running time is O(N), space is O(R) where R is a length of an alphabet.
    """
    # assume we have an ASCII string
    r = 256
    if len(string) > r:
        return False

    chars = [0] * r
    for i, char in enumerate(string):
        chars[ord(char)] += 1
        if chars[ord(char)] > 1:
            return False
    return True


def all_unique_bit(string):
    """
    Running time is O(N), required space is 1 byte only for ASCII string and 2 bytes for a Unicode string.
    Space usage is optimized using a bit vector.
    """
    # bit vector
    chars = 0
    for i, char in enumerate(string):
        # check if we have already seen this char
        if chars & (1 << ord(char)) > 0:
            return False
        else:
            chars |= (1 << ord(char))
    return True


if __name__ == '__main__':
    s = 'abcdefghatyk'
    assert not all_unique_set(s)
    assert not all_unique_list(s)
    assert not all_unique_bit(s)
    s = 'abcdefghtlk'
    assert all_unique_set(s)
    assert all_unique_list(s)
    assert all_unique_bit(s)