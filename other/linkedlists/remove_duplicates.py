# -*- coding: utf-8 -*-


def remove_duplicates(linked_list):
    """
    Runs in O(N) time, but requires O(N) space.
    """
    elems = set()
    prev = None
    for node in linked_list.iternodes():
        if node.value in elems:
            prev.next_node = node.next_node
        else:
            elems.add(node.value)
            prev = node


def remove_duplicates_slow(linked_list):
    """
    If we don't have a buffer we need to scan the linked list with 2 pointers searching
    for duplicates for each item.
    It will run O(N^2), but requires O(1) space.
    """
    current = linked_list.head
    while current:
        runner = current
        while runner:
            if runner.next_node and runner.next_node.value == current.value:
                # delete this duplicate
                runner.next_node = runner.next_node.next_node
            runner = runner.next_node
        current = current.next_node

if __name__ == '__main__':
    from linkedlist import LinkedList
    ll = LinkedList(['a', 'b', 'a', 'c', 'c', 'd', 'd'])
    remove_duplicates(ll)
    assert list(ll) == ['a', 'b', 'c', 'd']

    ll = LinkedList(['a', 'a', 'b', 'a', 'c', 'c', 'd', 'd'])
    remove_duplicates_slow(ll)
    assert list(ll) == ['a', 'b', 'c', 'd']