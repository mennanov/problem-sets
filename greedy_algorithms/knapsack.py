# -*- coding: utf-8 -*-

"""
See dynamic_programming/knapsack.py
"""
from dynamic_programming.knapsack import Item, Knapsack


class RobberyGreedy(object):
    """
    Knapsack greedy approach: it will not always give the best combination, but
    the running time is just O(NLogN)
    """

    def __init__(self, items):
        self.items = items

    def knapsack(self, weight):
        knapsack = Knapsack()
        # iterate through items by increasing weight
        for item in sorted(self.items):
            # if we have a room for this item in the knapsack
            if weight - knapsack.weight - item.weight >= 0:
                # add this item to the knapsack
                knapsack.add(item)
                if knapsack.weight == weight:
                    # if we have no room any more: stop iteration
                    break
        return knapsack


if __name__ == '__main__':
    items = (Item(6, 30), Item(3, 14), Item(4, 16), Item(2, 9))
    robbery = RobberyGreedy(items)
    assert robbery.knapsack(10).value == 39