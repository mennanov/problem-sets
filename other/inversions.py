# -*- coding: utf-8 -*-
"""
Assuming we have a list of integers and pointers i and j (i < j),
then inversion is when list[i] > [list[j].
For example in the list: [1, 3, 5, 2, 4, 6] inversions are: (3, 2), (5, 2), (5, 4)
"""


def inversions(x):
    """
    Naive approach which runs O(N**2).
    """
    for i in xrange(len(x)):
        for j in xrange(i, len(x)):
            if x[i] > x[j]:
                yield (x[i], x[j])


def inversions_fast(x):
    """
    Fast algorithm for finding inversions which runs O(NLogN).
    It uses the same idea as the merge sort:
    we divide input by half, search for inversions in the halves,
    sort these halves and search for split inversions.
    """
    if len(x) <= 1:
        # recursion tail: no inversions here
        return x, set()
    mid = len(x) / 2
    left = x[:mid]
    right = x[mid:]
    sorted_left, inversions_left = inversions_fast(left)
    sorted_right, inversions_right = inversions_fast(right)
    sorted_list, split_inversions = _merge(sorted_left, sorted_right)
    return sorted_list, inversions_left | inversions_right | split_inversions


def _merge(left, right):
    i = j = 0
    sorted_list = []
    invs = set()
    extra_invs = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            # no inversion there
            sorted_list.append(left[i])
            for k in extra_invs:
                # add extra inversions with elements from the right
                # which were already scanned before
                invs.add((left[i], right[k]))
            i += 1
        else:
            # the right element is less than the left one
            # it is an inversion
            sorted_list.append(right[j])
            invs.add((left[i], right[j]))
            # now every element on the left is greater than this element on the right
            # so it will generate more inversions with the next left elements
            extra_invs.append(j)
            j += 1
    # copy remained elements if input is odd length
    sorted_list += left[i:]
    sorted_list += right[j:]
    return sorted_list, invs



if __name__ == '__main__':
    x = [1, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10]
    assert len(list(inversions(x))) == 15
    assert len(inversions_fast(x)[1]) == 15