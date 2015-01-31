# -*- coding: utf-8 -*-

"""
Given a limited supply of coins we wish to make change for
a value v; that is, we wish to ﬁnd a set of coins whose total value is v. This might not be possible:
for instance, if the coins are 5 and 10 then we can make change for 15 but not for 12.
"""
from graph_shortest_path import memoize


class Change(object):
    """
    Coins change
    """

    def __init__(self, possible=True, coins=None):
        self.coins = coins if coins is not None else []
        self.sum = 0
        self.possible = possible

    def add(self, coin):
        self.coins.append(coin)
        self.sum += coin

    def __iter__(self):
        return iter(self.coins)

    def __str__(self):
        return str(self.coins) if self.possible else 'Change is impossible'

    def __eq__(self, other):
        return self.sum == other

    def copy(self):
        cp = type(self)()
        for c in self.coins:
            cp.add(c)
        return cp


class VendingMachine(object):
    def __init__(self, coins):
        self.coins = coins

    def make_change(self, price, banknote):
        amount = banknote - price
        if amount > 0:
            return self._change(amount)
        elif amount < 0:
            raise ValueError('You provided insufficient amount of money')
        else:
            return Change()

    @memoize
    def _change(self, amount, used=None):
        if used is None:
            used = frozenset()

        if amount == 0:
            return Change()

        for i, coin in enumerate(self.coins):
            if coin <= amount and i not in used:
                # find a perfect change for amount - coin
                subchange = self._change(amount - coin, used | {i}).copy()
                subchange.add(coin)
                # if subchange is at perfect amount - return it
                if subchange == amount:
                    return subchange
        return Change(False)


if __name__ == '__main__':
    vm = VendingMachine([5, 10, 3, 5, 3])
    assert list(vm.make_change(94, 100)) == [3, 3]