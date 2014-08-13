# -*- coding: utf-8 -*-
import math
import random
from collections import defaultdict


class Papadimitriou(object):
    """

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

    def run(self):
        n = len(self.vars)
        for _ in xrange(2 * int(math.log(n, 2))):
            # choose random initial assignment
            for i in xrange(1, n):
                self.vars[i] = random.choice([True, False])

            # evaluate each clause
            failed = self._solve(self.clauses)
            # print 'start local search', self.vars
            counter = 0
            while failed and counter < 2 * n ^ 2:
                # print 'failed: ', failed, len(failed)
                # flip random variable in a random failed clause and repeat local search on the corresponding clauses
                clause = random.sample(failed, 1)[0]
                proceed = True
                for var in clause:
                    if proceed:
                        var = abs(var)
                        # print 'flip', var, 'to', not self.vars[var]
                        self.vars[var] = not self.vars[var]
                        # iterate over involved clauses
                        failed_involved = self._solve(self.matches[var])

                        if failed_involved:
                            # add new failed clauses
                            # print 'flip not helped', var, failed_involved, len(failed_involved)
                            failed |= failed_involved
                        else:
                            # conflict with this particular variable is resolved
                            # print 'resolved conflicts for', var
                            failed -= self.matches[var]
                            proceed = False
                counter += 1
            if not failed:
                return True
        return False

    def _solve(self, clauses):
        failed = set()
        for clause in clauses:
            v1 = self.vars[clause[0]] if clause[0] > 0 else not self.vars[abs(clause[0])]
            v2 = self.vars[clause[1]] if clause[1] > 0 else not self.vars[abs(clause[1])]
            if not(v1 or v2):
                failed.add(clause)
        return failed

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as fp:
        n = int(fp.readline())
        clauses = []
        for i, line in enumerate(fp):
            data = line.split()
            clauses.append((int(data[0]), int(data[1])))

        p = Papadimitriou(clauses, [None] * (n + 1))
        print p.run()