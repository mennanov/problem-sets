# -*- coding: utf-8 -*-


def multiple_matrix(a, b):
    """
    Naive matrix multiplication approach for the matrices of the same square size.
    Each element of the each row from matrix A multiple with each element from each column in matrix B.
    Asymptotic analysis: O(N**3)
    """
    # the number of rows in matrix A must be the same
    # as the number of columns in matrix B
    assert len(a[0]) == len(b)
    m = len(a)
    n = len(a[0])
    q = len(b[0])
    # the resulting matrix size is m*q
    # create resulting matrix
    result = [[None] * q]
    for c in xrange(m - 1):
        result.append(result[c][:])
    # for each row of the matrix A
    for i in xrange(m):
        # for each column of the matrix B
        for j in xrange(q):
            s = 0
            # sum of each pairs of the two matrices
            for r in xrange(n):
                s += a[i][r] * b[r][j]
            result[i][j] = s
    return result


if __name__ == '__main__':
    a = [[1, 2], [3, 4], [5, 6]]
    b = [[7, 8, 9], [10, 11, 12]]
    assert multiple_matrix(a, b) == [[27, 30, 33], [61, 68, 75], [95, 106, 117]]