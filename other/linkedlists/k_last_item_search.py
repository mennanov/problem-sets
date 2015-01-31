# -*- coding: utf-8 -*-

"""
Find the k-th element from the tail of the list.
Suppose that the length of the linked list is unknown.
"""


def k_last_search_recursive(linked_list, k):
    """
    Use a recursion to count the depth of the linked list each recursive call.
    This method has drawbacks: we may hit a max recursion depth limit and we need
    an additional stack space for recursive calls.
    Time and space is O(N).
    """

    def find(node):
        if node is None:
            return 0
        # increase counter every recursive call
        depth = find(node.next_node)
        if isinstance(depth, tuple):
            # if the element is found just pass it up to the parent caller
            return depth
        elif depth + 1 == k:
            return depth + 1, node.value
        return depth + 1

    try:
        return find(linked_list.head)[1]
    except TypeError:
        raise IndexError(k)


def k_last_search_iterative(linked_list, k):
    """
    Tricky iterative approach: use 2 pointers p1 and p2.
    Move p2 k elements ahead from p1, then move them both to the right.
    When p2 hits the end of the list p1 will point exactly at the element we need.
    Runs in O(N) time, space is O(1).
    """
    p1, p2 = linked_list.head, linked_list.head

    # move p2 k elements ahead
    for i in xrange(k):
        try:
            p2 = p2.next_node
        except AttributeError:
            # the list is even shorter than k
            raise IndexError(k)

    # move both pointers
    while p2:
        p1 = p1.next_node
        p2 = p2.next_node

    return p1.value


if __name__ == '__main__':
    from linkedlist import LinkedList

    ll = LinkedList(['a', 'b', 'a', 'q', 'c', 'e', 'd'])
    assert k_last_search_recursive(ll, 3) == 'c'
    assert k_last_search_iterative(ll, 3) == 'c'