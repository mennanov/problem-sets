# -*- coding: utf-8 -*-


def power(number, pow):
    """
    Integer power naive implementation which runs O(N)
    """
    result = 1
    for i in xrange(pow):
        result *= number
    return result


def power_fast(number, pow):
    """
    Exponentiation by squaring:
    Integer power divide&conquer implementation which runs O(LogN)
    by halving the input pow each call.
    """
    if pow == 1:
        return number
    # reduce the problem by the factor of 2
    result = power_fast(number * number, pow / 2)
    if pow % 2 == 0:
        return result
    else:
        return result * number
    return result


if __name__ == '__main__':
    assert power(2, 8) == 256
    assert power_fast(2, 5) == 32