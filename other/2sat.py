# -*- coding: utf-8 -*-
import math
import random
from collections import defaultdict


class Papadimitriou(object):
    """
    2-SAT Papadimitriou's randomized algorithm which runs O(N^2LogN) and answers the satisfiability request
    with 1 - 1/n probability, where n is the number of variables.
    """

    def __init__(self, clauses, vars):
        self.clauses = clauses
        self.vars = vars
        # prepare the matching data
        self.matches = self._match_vars_to_clauses(clauses)

    @staticmethod
    def _match_vars_to_clauses(clauses):
        """
        For every variable create a list of clauses where this variable occurs.
        """
        matches = defaultdict(lambda: set())
        for c in clauses:
            matches[abs(c[0])].add(c)
            matches[abs(c[1])].add(c)
        return matches

    def preprocess(self):
        """
        Remove clauses which don't make sense.
        It may significantly improve the running time of the algorithm because it may decently shrink the input
        data: ex., for 600000 clauses this preprocessing step may shrink it to just 11!
        """
        while True:
            delete = []
            for var, clauses in self.matches.iteritems():
                # check if this variable is always positive (not negated)
                always_positive = all(c[0] == var or c[1] == var for c in clauses)
                if always_positive:
                    # remove these clauses and this variable
                    self.clauses -= clauses
                    # remove the neighbour matches
                    for c in clauses:
                        neighbour = abs(c[0]) if var == abs(c[1]) else abs(c[1])
                        self.matches[neighbour].remove(c)
                    delete.append(var)
                    continue

                # check if this variable is always negative
                always_negative = all(c[0] == -var or c[1] == -var for c in clauses)
                if always_negative:
                    # remove these clauses and this variable
                    self.clauses -= clauses
                    # remove the neighbour matches
                    for c in clauses:
                        neighbour = abs(c[0]) if var == abs(c[1]) else abs(c[1])
                        self.matches[neighbour].remove(c)
                    delete.append(var)

            if delete:
                for d in delete:
                    del self.matches[d]
            else:
                break

    def run(self):
        n = len(self.vars)
        for _ in xrange(int(math.log(n, 2))):
            # choose random initial assignment
            for i in xrange(1, n):
                self.vars[i] = random.choice([True, False])

            # evaluate each clause
            failed = self._solve(self.clauses)
            # as in classical Papadimitriou's algorithm we repeat 2 * n ^ 2 times to be able to report
            # unsatisfiability of the data in the end if solution is still not found
            counter = 0
            while failed and counter < 2 * n ^ 2:
                # pick a random failed clause and repeat local search on the clauses
                # which were affected by flipping the variable
                clause = random.choice(tuple(failed))
                proceed = True
                for var in clause:
                    # flip each variable in a clause
                    if proceed:
                        var = abs(var)
                        # flip the value of a variable
                        self.vars[var] = not self.vars[var]
                        # iterate over involved clauses
                        failed_involved = self._solve(self.matches[var])
                        if failed_involved:
                            # add new failed clauses
                            failed |= failed_involved
                        else:
                            # conflict with this particular variable is resolved
                            failed -= self.matches[var]
                            proceed = False
                counter += 1
            if not failed:
                # we have no failed clauses: all of them resolve to True
                return True
        # we could not find the solution within 2 * n ^ 2 steps: report that solution does not exist
        # with probability 1 - 1/n (so it may be wrong in rare cases).
        return False

    def _solve(self, clauses):
        """
        Evaluate the given expressions and return failed ones.
        """
        failed = set()
        for clause in clauses:
            v1 = self.vars[clause[0]] if clause[0] > 0 else not self.vars[abs(clause[0])]
            v2 = self.vars[clause[1]] if clause[1] > 0 else not self.vars[abs(clause[1])]
            if not (v1 or v2):
                failed.add(clause)
        return failed


if __name__ == '__main__':
    with open('2sat.txt') as fp:
        n = int(fp.readline())
        clauses = set()
        for i, line in enumerate(fp):
            data = line.split()
            clauses.add((int(data[0]), int(data[1])))

        p = Papadimitriou(clauses, [None] * (n + 1))
        p.preprocess()
        assert p.run()