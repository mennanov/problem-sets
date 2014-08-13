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
        matches = defaultdict(lambda: [])
        for c in clauses:
            matches[abs(c[0])].append(c)
            matches[abs(c[1])].append(c)
        return matches

    def run(self):
        n = len(self.vars)
        for _ in xrange(int(math.log(n, 2))):
            # choose random initial assignment
            for i in xrange(1, n):
                self.vars[i] = random.choice([True, False])

            for j in xrange(2 * n ^ 2):
                # perform local search
                failed = []
                for c in self.clauses:
                    if not self._solve(c):
                        failed.append(c)

                if not failed:
                    # the problem is solvable
                    return True
                else:
                    # flip random variable in a random failed clause and repeat local search
                    random_clause = random.choice(failed)
                    var = abs(random_clause[random.choice([0, 1])])
                    self.vars[var] = not self.vars[var]
        return False

    def _solve(self, clause):
        v1 = self.vars[clause[0]] if clause[0] > 0 else not self.vars[abs(clause[0])]
        v2 = self.vars[clause[1]] if clause[1] > 0 else not self.vars[abs(clause[1])]
        return v1 or v2

if __name__ == '__main__':
    with open('test.txt') as fp:
        n = int(fp.readline())
        clauses = []
        vars = [False] * (n + 1)
        for i, line in enumerate(fp):
            data = line.split()
            clauses.append((int(data[0]), int(data[1])))

        p = Papadimitriou(clauses, vars)
        print p.run()