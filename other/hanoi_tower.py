# -*- coding: utf-8 -*-


class Tower(object):
    """
    A tower class.
    """

    def __init__(self, disks=()):
        self.disks = []
        for disk in disks:
            self.add(disk)

    def add(self, disk):
        self.disks.append(disk)

    def move_top_to(self, destination):
        disk = self.disks.pop()
        destination.add(disk)

    def move_disks(self, n, dest, buff):
        if n > 0:
            # move n-1 disks from this tower to the buffer tower using destination tower as a buffer
            self.move_disks(n - 1, buff, dest)
            # move the remained one disk (the largest) to the destination tower
            self.move_top_to(dest)
            # move disks from buffer tower to destination tower using this tower as a buffer
            buff.move_disks(n - 1, dest, self)


if __name__ == '__main__':
    towers = Tower(['disk', 'disk', 'disk', 'disk']), Tower(), Tower()
    towers[0].move_disks(4, towers[2], towers[1])
    assert len(towers[2].disks) == 4