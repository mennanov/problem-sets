# -*- coding: utf-8 -*-
"""
Compute an n-th Fibonacci sequence number in O(LogN) time.
There is an equivalence: Matrix([[1, 1], [1, 0]]) ** n = Matrix([[Fib(n + 1), Fib(n)], [Fib(n), Fib(n - 1)]]).
So all we need to do is to compute the n-th power of the initial matrix and get the second item in the first row -
that will be an answer.
It exists an efficient approach of computing the n-th power of a number called "Exponentiation by squaring".
We will use this idea to compute the n-th power of matrix.
"""


class Matrix(list):
    def __mul__(self, other):
        # assume "other" is also a Matrix or a list-like object
        n = len(self)
        m = len(self[0])
        q = len(other[0])
        assert len(other) == m
        result = []
        for i in xrange(n):
            row = []
            for j in xrange(q):
                cell = 0
                for k in xrange(m):
                    cell += self[i][k] * other[k][j]
                row.append(cell)
            result.append(row)

        return Matrix(result)


def exp(operand, e):
    """
    Exponentiation by squaring. O(LogN) complexity.
    """
    if e < 0:
        # special case
        return 1 / exp(operand, -e)
    elif e == 1:
        return operand
    r = exp(operand, e / 2)
    result = r * r
    if e % 2 == 1:
        # if exponent is odd
        result *= operand
    return result


def fib(n):
    """
    Fibonacci sequence n-th number in O(LogN) time.
    """
    if n < 2:
        return n
    return exp(Matrix([[1, 1], [1, 0]]), n - 1)[0][0]


if __name__ == '__main__':
    assert fib(100) == 354224848179261915075
