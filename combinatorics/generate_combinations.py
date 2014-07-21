# -*- coding: utf-8 -*-


def combinations_2k(items):
    """
    Generate 2-length combinations of a given sequence in lexicographic order.
    """
    l = len(items)
    for i in xrange(l - 1):
        for j in xrange(i + 1, l):
            yield items[i], items[j]


def combinations_3k(items):
    """
    Generate 3-length combinations of a given sequence in lexicographic order.
    """
    l = len(items)
    for i in xrange(l - 2):
        for j in xrange(i + 1, l - 1):
            for k in xrange(j + 1, l):
                yield items[i], items[j], items[k]


def xcombinations_lex(items, length, start=0):
    """
    Recursively generate combinations of a given length in lexicographic order.
    """
    if length == 0:
        yield ()
    else:
        for i in xrange(start, len(items) - length + 1):
            for subcombination in xcombinations_lex(items, length - 1, i + 1):
                yield (items[i], ) + subcombination


def combinations_lex(items, length, start=0):
    """
    Return all combinations in lexicographic order as a list
    """
    result = []
    if length == 1:
        for i in xrange(start, len(items)):
            result.append((items[i],))
    else:
        for i in xrange(start, len(items) - length + 1):
            for subcombination in combinations_lex(items, length - 1, i + 1):
                result.append((items[i],) + subcombination)
    return result


def xcombinations_lex_all(items):
    """
    Generate all possible 2^n - 1 combinations in lexicographic order.
    """
    for l in xrange(1, len(items) + 1):
        for c in xcombinations_lex(items, l):
            yield c


def xcombinations_bin(items):
    """
    Generate all possible 2^n - 1 combinations using binary counting.
    """
    for i in xrange(1, 2 ** len(items)):
        combination = ()
        # iterate over bits of this number
        for pos, bit in enumerate((i >> p & 1 for p in xrange(i.bit_length()))):
            if bit == 1:
                combination += (items[pos],)
        yield combination


def xcombinations_gray(items):
    """
    Generate all possible 2^n - 1 combinations using Gray code.
    """
    for i in xrange(1, 2 ** len(items)):
        combination = ()
        # convert to Gray code
        i ^= i >> 1
        # iterate over bits of this number
        for pos, bit in enumerate((i >> p & 1 for p in xrange(i.bit_length()))):
            if bit == 1:
                combination += (items[pos],)
        yield combination


def xcombinations_prefix(items, prefix=(), start=0):
    """
    Generate combinations of given length using prefix recurrence
    """
    for i in range(start, len(items)):
        combination = prefix + (items[i],)
        yield combination
        for c in xcombinations_prefix(items, combination, i + 1):
            yield c


if __name__ == '__main__':
    from math import factorial

    seq = range(1, 5)
    n = len(seq)
    k = 2
    assert len(list(combinations_2k(seq))) == factorial(n) / (factorial(k) * factorial(n - k))
    k = 3
    assert len(list(combinations_3k(seq))) == factorial(n) / (factorial(k) * factorial(n - k))
    assert len(list(xcombinations_lex(seq, 3))) == len(list(combinations_3k(seq)))
    assert len(combinations_lex(seq, 3)) == len(list(combinations_3k(seq)))
    assert set(list(xcombinations_bin(seq))) == set(list(xcombinations_gray(seq))) == set(
        list(xcombinations_lex_all(seq)))
    assert len(list(xcombinations_prefix(seq))) == 15
