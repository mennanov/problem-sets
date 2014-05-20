# -*- coding: utf-8 -*-
import math


def multiple(a, b):
    """
    Naive implementation of decimal integer multiplication.
    It runs ~O(2N*M), where N = len(a) and M = len(b).
    This algorithm seems to be slow (it may run quadratic if N==M)
    """
    a, b = str(a), str(b)
    # intermediary results
    rows = []
    for i in xrange(len(b) - 1, -1, -1):
        # reversed intermediate row
        row = [0] * (len(b) - i - 1)
        carry = 0
        for j in xrange(len(a) - 1, -1, -1):
            m = int(b[i]) * int(a[j]) + carry
            r = m % 10
            carry = m // 10
            row.append(r)
        row.append(carry)
        rows.append(row)
    # add rows
    sum_row = [0] * len(rows[0])
    for i in xrange(len(rows)):
        row = rows[i]
        new_sum_row = []
        carry = 0
        for j in xrange(len(row)):
            try:
                c = sum_row[j]
            except IndexError:
                c = 0
            s = c + row[j] + carry
            r = s % 10
            carry = s // 10
            new_sum_row.append(r)
        new_sum_row.append(carry)
        sum_row = new_sum_row[:]
    sum_row.reverse()
    return int(''.join([str(x) for x in sum_row]))


def multiple_karatsuba(x, y):
    """
    Recursive divide&conquer algorithm for integer multiplication for base 10.
    It runs O(N**Log3) which is faster than O(N**2) as in naive approach.
    """
    if x < 10 or y < 10:
        # this is a tail of the recursion:
        # integers are simple enough to perform a regular multiplication
        return x * y

    # convert to string to use Python slicing
    x, y = str(x), str(y)
    # divide the both integers in to half (ceil is for the odd numbers)
    a, b = int(x[:int(math.ceil(len(x) / 2.0))]), int(x[int(math.ceil(len(x) / 2.0)):])
    c, d = int(y[:int(math.ceil(len(y) / 2.0))]), int(y[int(math.ceil(len(y) / 2.0)):])
    # perform arithmetic steps
    step1 = multiple_karatsuba(a, c)
    step2 = multiple_karatsuba(b, d)
    step3 = multiple_karatsuba((a + b), (c + d))
    step4 = step3 - step2 - step1
    # get the longest input length
    m = max(len(x), len(y))/2
    # perform addition
    return step1 * (10 ** (m*2)) + step2 + step4 * (10 ** m)




if __name__ == '__main__':
    assert multiple(5678, 1234) == 5678 * 1234
    assert multiple(11, 11) == 11 * 11
    assert multiple_karatsuba(5678, 1234) == 5678 * 1234