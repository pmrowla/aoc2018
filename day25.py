#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 25 module."""
from __future__ import division, print_function

import itertools
from heapq import heappush, heappop


def distance(p1, p2):
    return sum([abs(a - b) for a, b in zip(p1, p2)])


def adjacent(points, p):
    adj = set()
    for p2 in points:
        if p == p2:
            continue
        if distance(p, p2) <= 3:
            adj.add(p2)
    return adj


q = []
entries = {}
counter = itertools.count()


def add_update_prio(p, prio):
    if p in entries:
        # invalidate existing entry
        entry = entries[p]
        entry[-1] = False
    entry = [prio, next(counter), p, True]
    entries[p] = entry
    heappush(q, entry)


def pop_min_prio():
    while q:
        _, _, p, valid = heappop(q)
        if p in entries and valid:
            del entries[p]
            return p
    return None


def dijkstra(points, p, verbose=False):
    dist = {}
    prev = {}
    add_update_prio(p, 0)
    dist[p] = 0
    while entries:
        u = pop_min_prio()
        if not u:
            break
        for v in points:
            alt = distance(u, v)
            if alt <= 3 and (v not in dist or alt < dist[v]):
                dist[v] = alt
                prev[v] = u
                add_update_prio(v, alt)
    return dist, prev


def process(puzzle_input, verbose=False):
    points = set()
    for line in puzzle_input:
        points.add(tuple([int(x) for x in line.split(',')]))
    if verbose:
        [print(p) for p in points]
    cons = []
    while points:
        p = points.pop()
        dist, _ = dijkstra(points, p)
        c = set(dist.keys())
        points.difference_update(c)
        cons.append(c)
    if verbose:
        print(cons)
    return len(cons), None


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
