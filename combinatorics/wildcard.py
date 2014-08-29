# -*- coding: utf-8 -*-


def wildcard(pattern):
    """
    Given a string of 0s, 1s, and ?s (wildcards), generate all 0-1 strings that match the pattern
    """
    wildcards = pattern.count('?')
    alphabet = ['0', '1']

    def xcombinations(items, length):
        if length == 0:
            yield []
        else:
            for i in xrange(len(items)):
                for sc in xcombinations(items, length - 1):
                    yield [items[i]] + sc

    for combination in xcombinations(alphabet, wildcards):
        buff = ''
        for c in pattern:
            if c == '?':
                buff += combination.pop()
            else:
                buff += c
        yield buff


if __name__ == '__main__':
    assert list(wildcard('1??0')) == ['1000', '1100', '1010', '1110']