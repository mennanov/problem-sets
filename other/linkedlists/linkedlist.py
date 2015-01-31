# -*- coding: utf-8 -*-


class LinkedList(object):
    """
    Singly linked list: fast append-left and pop-left operations.
    """
    class Node(object):

        def __init__(self, value, next_node=None):
            self.next_node = next_node
            self.value = value

    def __init__(self, iterable=None):
        self.head = None
        self.length = 0
        if iterable:
            for i in iterable:
                self.append(i)

    def append(self, value):
        """
        Appends to the right tail of the list.
        Takes O(N) time.
        """
        try:
            node = self._get_node(-1)
            node.next_node = self.Node(value)
        except IndexError:
            self.head = self.Node(value)
        self.length += 1

    def appendleft(self, value):
        """
        Appends to the left head of the list.
        Takes O(1) time.
        """
        node = self.Node(value, self.head)
        self.head = node

    def __len__(self):
        """
        Returns the length of the list.
        Takes O(1) time.
        """
        return self.length

    def iternodes(self):
        """
        Nodes generator.
        Runs in O(N) time.
        """
        node = self.head
        while node:
            yield node
            node = node.next_node

    def _get_nodes_pair(self, index):
        """
        Get the node and its previous sibling node by its index.
        Runs in O(N) time.
        """
        node = None
        prev_node = None
        if index < 0:
            # support negative indexes
            index += len(self)
        c = 0
        for c, node in enumerate(self.iternodes()):
            if c >= index:
                break
            else:
                prev_node = node
        if index == c and node:
            return node, prev_node
        else:
            raise IndexError(index)

    def _get_node(self, i):
        return self._get_nodes_pair(i)[0]

    def __getitem__(self, item):
        return self._get_node(item).value

    def __delitem__(self, key):
        """
        Delete item by its index.
        Takes O(N) time.
        """
        node, prev_node = self._get_nodes_pair(key)
        value = node.value
        if node.next_node:
            # intermediate node
            node.value = node.next_node.value
            node.next_node = node.next_node.next_node
        elif prev_node:
            # tail node
            prev_node.next_node = None
        else:
            # single head node
            self.head = None
        self.length -= 1
        return value

    def popleft(self):
        """
        Pop element from the left head of the list.
        Takes O(1) time.
        """
        try:
            return self.__delitem__(0)
        except IndexError:
            raise IndexError('pop from empty LinkedList')

    def pop(self):
        """
        Pop element from the right tail of the list.
        Takes O(N) time.
        """
        try:
            return self.__delitem__(len(self) - 1)
        except IndexError:
            raise IndexError('pop from empty LinkedList')

    def __iter__(self):
        for node in self.iternodes():
            yield node.value

    def __repr__(self):
        return 'LinkedList({})'.format(repr(list(self)))


if __name__ == '__main__':
    linked_list = LinkedList(['a', 'b', 'c', 'd'])
    assert list(linked_list) == ['a', 'b', 'c', 'd']
    del linked_list[0]
    assert list(linked_list) == ['b', 'c', 'd']
    assert len(linked_list) == 3
    assert linked_list.popleft() == 'b'
    assert list(linked_list) == ['c', 'd']
    assert linked_list.pop() == 'd'
    assert list(linked_list) == ['c']
    linked_list.appendleft('a')
    assert list(linked_list) == ['a', 'c']