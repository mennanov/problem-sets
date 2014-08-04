# -*- coding: utf-8 -*-

"""
Detect if the linked list is a palindrome.
"""


def is_palindrome_stack(linked_list):
    """
    Fill in the stack with all the items from the linked list in one pass.
    Then make a second iteration and compare items.
    It runs in O(N) time and needs the same amount of space.
    """
    stack = []
    node = linked_list.head
    # fill in the stack
    while node:
        stack.append(node.value)
        node = node.next_node

    node = linked_list.head
    # check the order
    while node:
        if node.value != stack.pop():
            return False
        node = node.next_node

    return True


def is_palindrome_stack_optimized(linked_list):
    """
    Use the slow/fast runner technique to decrease the running time from 2N to N and
    the space to N/2. However in terms of the big O notation everything remains the same.
    """
    # use stack only for the first half of the list
    stack = []
    slow, fast = linked_list.head, linked_list.head
    # fill in the stack
    while fast and fast.next_node:
        # append the value from the slow pointer
        stack.append(slow.value)
        slow = slow.next_node
        fast = fast.next_node.next_node

    # at that moment the slow pointer points at the middle of the list
    while slow:
        if slow.value != stack.pop():
            print slow.value
            return False
        slow = slow.next_node

    return True


if __name__ == '__main__':
    from linkedlist import LinkedList

    ll = LinkedList(['a', 'b', 'b', 'a'])
    assert is_palindrome_stack(ll)
    assert is_palindrome_stack_optimized(ll)