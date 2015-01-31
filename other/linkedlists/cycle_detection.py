# -*- coding: utf-8 -*-

"""
Detect if a linked list has a cycle in linear time.
A linked list has a cycle if one of the nodes points back to any other already seen node.
"""


def has_cycle(linked_list):
    """
    Use a slow runner/fast runner approach: 2 pointers, one runs 1 step at a time,
    another runs 2 steps at a time. If they meet - we have a cycle.
    """
    slow, fast = linked_list.head, linked_list.head.next_node
    while fast and fast.next_node:
        if slow == fast:
            return True
        slow = slow.next_node
        fast = fast.next_node.next_node
    return False


if __name__ == '__main__':
    from linkedlist import LinkedList

    ll = LinkedList(['a', 'b', 'a', 'q', 'c', 'e', 'd'])
    # add a cyclic node manually
    node = ll.head
    while True:
        if not node.next_node:
            node.next_node = LinkedList.Node('cyclic node', ll.head)
            break
        node = node.next_node

    assert has_cycle(ll)