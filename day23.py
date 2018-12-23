#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 23 module."""
from __future__ import division, print_function

import re

from z3 import If, Int, Optimize


def pprint(grid):
    for row in grid:
        print(''.join([x[1] for x in row]))


def distance(p1, p2):
    return sum([abs(a - b) for a, b in zip(p1, p2)])


def zabs(x):
    return If(x >= 0, x, -x)


def zdist(p1, p2):
    return zabs(p1[0] - p2[0]) + zabs(p1[1] - p2[1]) + zabs(p1[2] - p2[2])


def process(puzzle_input, verbose=False):
    nanobots = []
    for line in puzzle_input:
        m = re.match('^pos=<(?P<pos>-?\d+,-?\d+,-?\d+)>, r=(?P<r>\d+)$', line)
        if m:
            pos = tuple([int(x) for x in m.group('pos').split(',')])
            r = int(m.group('r'))
            nanobots.append((pos, r))
    nanobots = sorted(nanobots, key=lambda x: x[1])
    if verbose:
        [print('pos=<{}>, r={}'.format(p, r)) for p, r in nanobots]
    p1 = sum([distance(nanobots[-1][0], p) <= nanobots[-1][1] for p, _ in nanobots])

    in_range = [Int('in_range_{}'.format(i)) for i in range(len(nanobots))]
    range_count = Int('range_count')
    x = Int('x')
    y = Int('y')
    z = Int('z')
    s = Optimize()
    for i, (p, r) in enumerate(nanobots):
        s.add(in_range[i] == If(zdist((x, y, z), p) <= r, 1, 0))
    s.add(range_count == sum(in_range))
    dist = Int('dist')
    s.add(dist == zdist((0, 0, 0), (x, y, z)))
    print('solving w/z3...')
    s.maximize(range_count)
    s.minimize(dist)
    s.check()
    m = s.model()
    if verbose:
        print(m)

    return p1, m[dist].as_long()


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    parser.add_argument('-v', '--verbose', '-d', '--debug',
                        action='store_true', dest='verbose', help='verbose output')
    args = parser.parse_args()
    try:
        puzzle_input = [line.strip() for line in fileinput.input(args.infile)]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print('Part one: {}'.format(p1))
        print('Part two: {}'.format(p2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
