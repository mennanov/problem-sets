# -*- coding: utf-8 -*-
from collections import defaultdict


class UnionFind(object):
    """
    Union-find fast implementation
    """

    def __init__(self):
        self.id = {}
        self.rank = defaultdict(int)

    def find(self, item):
        if item in self.id:
            while item != self.id[item]:
                # path compression by halving
                self.id[item] = self.id[self.id[item]]
                item = self.id[item]
        else:
            self.id[item] = item
        return item

    def union(self, p, q):
        i, j = self.find(p), self.find(q)
        if i == j:
            return
        # make the root of the smaller rank point to the root of the larger rank
        if self.rank[i] < self.rank[j]:
            self.id[i] = j
        elif self.rank[i] > self.rank[j]:
            self.id[j] = i
        else:
            self.id[j] = i
            # rank increases only when the two trees of the equal ranks are fused
            self.rank[i] += 1

    def connected(self, p, q):
        return self.find(p) == self.find(q)


if __name__ == '__main__':
    uf = UnionFind()
    uf.union(1, 0)
    uf.union(2, 1)
    uf.union(3, 2)
    uf.union(5, 4)
    uf.union(6, 5)
    uf.union(7, 5)
    assert uf.find(7) == uf.find(5)