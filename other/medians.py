# -*- coding: utf-8 -*-

"""
Medians problem: assume that we have a stream of integers coming one at a time.
The goal is to compute the median element of these integers every time the new integer comes.
We already have a fast selection algorithm which runs O(N), but in this particular problem the
overall running time will be O(N^2) as we will have to execute selection routine for every new coming integer.
But there is a faster approach below which runs only O(NLogN) and uses 2 binary heaps to compute medians.
"""

import heapq
from math import ceil


class MaxHeap(object):
    def __init__(self, x):
        self.heap = [-e for e in x]
        heapq.heapify(self.heap)

    def push(self, value):
        heapq.heappush(self.heap, -value)

    def pop(self):
        return -heapq.heappop(self.heap)

    def __getitem__(self, item):
        return -self.heap[item]

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return str([-x for x in self.heap])


class MinHeap(object):
    def __init__(self, x):
        self.heap = x
        heapq.heapify(self.heap)

    def push(self, value):
        heapq.heappush(self.heap, value)

    def pop(self):
        return heapq.heappop(self.heap)

    def __getitem__(self, item):
        return self.heap[item]

    def __len__(self):
        return len(self.heap)

    def __str__(self):
        return str(self.heap)


def medians_sum(fp):
    """
    Compute the medians sum of the integer stream from a file-like object
    using \n as a delimiter (one number at a line).
    """
    left_heap = MaxHeap([])
    right_heap = MinHeap([])
    length = 0
    result_sum = 0
    while True:
        line = fp.readline()
        if line:
            number = int(line)
            # choose the heap to populate
            try:
                left_max = left_heap[0]
            except IndexError:
                left_max = float('-inf')
            if number < left_max:
                # populate left heap
                left_heap.push(number)
            else:
                # populate right heap
                right_heap.push(number)
            # restore the balance between heaps
            if len(left_heap) - len(right_heap) > 1:
                right_heap.push(left_heap.pop())
            elif len(right_heap) - len(left_heap) > 1:
                left_heap.push(right_heap.pop())
            length += 1
            m = ceil(length / 2.0)
            if m > len(left_heap):
                # median is at the right heap
                median = right_heap[0]
            else:
                # median is at the left heap
                median = left_heap[0]
            result_sum += median
        else:
            break
    return result_sum % 10000


if __name__ == '__main__':
    from StringIO import StringIO

    fp = StringIO('\n'.join(str(x) for x in [3, 7, 4, 1, 2, 6, 5]))
    assert medians_sum(fp)
