# -*- coding: utf-8 -*-
"""
Given the list of jobs with their weights (priorities) and length (time durations).
The weighted completion time of a job is a sum of all the previous jobs lengths + the current one.
"""
from abc import ABCMeta, abstractmethod


class JobAbstract(object):
    """
    Job class stores the information about its weight and length and
    also should handle compares with other jobs
    """
    __metaclass__ = ABCMeta

    def __init__(self, weight, length):
        self.weight = weight
        self.length = length

    def __repr__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.weight, self.length)

    @abstractmethod
    def __cmp__(self, other):
        pass


class JobDiff(JobAbstract):
    """
    Job with decreasing order of the difference (weight - length)
    """

    def __str__(self):
        return '{}, {}, {}'.format(self.weight, self.length, self.weight - self.length)

    def __cmp__(self, other):
        if self.weight - self.length > other.weight - other.length:
            return 1
        elif self.weight - self.length < other.weight - other.length:
            return -1
        else:
            return cmp(self.weight, other.weight)


class JobRatio(JobAbstract):
    """
    Job with decreasing order of the ratio (weight/length)
    """

    def __str__(self):
        return '{}, {}, {}'.format(self.weight, self.length, float(self.weight) / self.length)

    def __cmp__(self, other):
        if float(self.weight) / self.length > float(other.weight) / other.length:
            return 1
        elif float(self.weight) / self.length < float(other.weight) / other.length:
            return -1
        else:
            return cmp(self.weight, other.weight)


def schedule(jobs):
    completion_time = 0
    completion_sum = 0
    # sort all the jobs by the rules in the Job class
    for job in sorted(jobs, reverse=True):
        completion_sum += job.weight * (job.length + completion_time)
        completion_time += job.length
    return completion_sum


if __name__ == '__main__':
    jobs = [JobDiff(48, 14), JobDiff(4, 90), JobDiff(64, 22), JobDiff(54, 66), JobDiff(46, 6)]
    assert schedule(jobs) == 11336

    jobs = [JobRatio(48, 14), JobRatio(4, 90), JobRatio(64, 22), JobRatio(54, 66), JobRatio(46, 6)]
    assert schedule(jobs) == 10548