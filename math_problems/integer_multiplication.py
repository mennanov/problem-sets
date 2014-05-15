# -*- coding: utf-8 -*-


def multiple(a, b):
    """
    Naive implementation of decimal integer multiplication.
    It runs O(2N*N).
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


if __name__ == '__main__':
    assert multiple(5678, 1234) == 7006652