# -*- coding: utf-8 -*-


def multiple_matrix(a, b):
    """
    Naive matrix multiplication approach for the matrices.
    Each element of the each row from matrix A multiple with each element from each column in matrix B.
    Asymptotic analysis: O(N**3)
    """
    m = len(a)
    n = len(a[0])
    q = len(b[0])
    assert m == q, 'the number of rows in matrix A must be the same as the number of columns in matrix B'
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


class Matrix(object):
    """
    Simple square matrix m*n where m == n.
    """

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)

    def __len__(self):
        # size of the matrix
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __sub__(self, other):
        """
        Subtract two matrices of the same size
        """
        size = len(self)
        # create resulting matrix
        result = [[None] * size]
        for c in xrange(size - 1):
            result.append(result[c][:])
        for i in xrange(size):
            for j in xrange(size):
                result[i][j] = self[i][j] - other[i][j]
        return Matrix(result)

    def __add__(self, other):
        """
        Add two matrices of the same size
        """
        size = len(self)
        # create resulting matrix
        result = [[None] * size]
        for c in xrange(size - 1):
            result.append(result[c][:])
        for i in xrange(size):
            for j in xrange(size):
                result[i][j] = self[i][j] + other[i][j]
        return Matrix(result)

    def split(self):
        """
        Split the matrix into 4 pieces
        """
        size = len(self)
        if size == 2:
            # split 2x2 matrix into 4 integers
            return self[0][0], self[0][1], self[1][0], self[1][1]
        else:
            a, b, c, d = [], [], [], []
            for i in xrange(size):
                for j in xrange(size):
                    if i < size / 2:
                        # populate A or B
                        if j < size / 2:
                            # left top corner
                            a.append(self[i][j])
                        else:
                            # right top corner
                            b.append(self[i][j])
                    else:
                        # populate C or D
                        if j < size / 2:
                            # left bottom corner
                            c.append(self[i][j])
                        else:
                            # right bottom corner
                            d.append(self[i][j])

            def list2matrix(l):
                # split elements into size / 2 chunks
                return [l[i: i + size / 2] for i in xrange(0, len(l), size / 2)]

            return Matrix(list2matrix(a)), Matrix(list2matrix(b)), Matrix(list2matrix(c)), Matrix(list2matrix(d))

    @staticmethod
    def join(lt, rt, lb, rb):
        """
        Join 4 pieces into one matrix.
        """
        if isinstance(lt, int):
            # 2x2 matrix
            return Matrix([[lt, rt], [lb, rb]])
        # size of the new matrix
        size = len(lt) * 2
        # create resulting matrix
        result = [[None] * size]
        for c in xrange(size - 1):
            result.append(result[c][:])
        # populate the matrix
        for i in xrange(size):
            for j in xrange(size):
                if i < size / 2:
                    if j < size / 2:
                        # left top corner
                        result[i][j] = lt[i][j]
                    else:
                        # right top corner
                        result[i][j] = rt[i][j % (size / 2)]
                else:
                    if j < size / 2:
                        # left bottom corner
                        result[i][j] = lb[i % (size / 2)][j % (size / 2)]
                    else:
                        # right bottom corner
                        result[i][j] = rb[i % (size / 2)][j % (size / 2)]
        return Matrix(result)

    def __mul__(self, other):
        """
        Strassen's fast multiplication algorithm for square even sized matrices.
        This requirement is based on the approach of the algorithm: it divides the matrix into 4
        matrices of the same size.
        It runs O(N**2.81) which is subqubic because it needs only 7 multiplications
        in each recursion call instead of 8, so it saves significant time with large inputs.
        It begins to beat the naive approach when the input matrix size is 64x64.
        """
        # split matrices into 4 pieces
        a, b, c, d = self.split()
        e, f, g, h = other.split()
        # calculate seven products
        p1 = a * (f - h)
        p2 = (a + b) * h
        p3 = (c + d) * e
        p4 = d * (g - e)
        p5 = (a + d) * (e + h)
        p6 = (b - d) * (g + h)
        p7 = (a - c) * (e + f)
        # calculate 4 corners of the new matrix
        lt = p5 + p4 - p2 + p6
        rt = p1 + p2
        lb = p3 + p4
        rb = p1 + p5 - p3 - p7
        return self.join(lt, rt, lb, rb)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            return self.data == other.data
        else:
            raise TypeError


if __name__ == '__main__':
    a = [[1, 2], [3, 4], [5, 6]]
    b = [[7, 8, 9], [10, 11, 12]]
    assert multiple_matrix(a, b) == [[27, 30, 33], [61, 68, 75], [95, 106, 117]]

    c = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    d = Matrix([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
    e = Matrix([[90, 100, 110, 120], [202, 228, 254, 280], [314, 356, 398, 440], [426, 484, 542, 600]])
    assert c * d == e
