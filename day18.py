#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 18 module."""
from __future__ import division, print_function

import re

from collections import Counter


def pprint(grid):
    [print(''.join(row)) for row in grid]


def adjacent(grid, x, y):
    adj = []
    for i, j in [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]:
        try:
            if i >= 0 and j >= 0:
                adj.append(grid[j][i])
        except IndexError:
            pass
    return Counter(adj)


def run_one(grid, verbose=False):
    new_grid = []
    for y, row in enumerate(grid):
        new_row = []
        for x, c in enumerate(row):
            adj = adjacent(grid, x, y)
            if c == '.' and adj['|'] >= 3:
                new_row.append('|')
            elif c == '|' and adj['#'] >= 3:
                new_row.append('#')
            elif c == '#' and not (adj['|'] >= 1 and adj['#'] >= 1):
                new_row.append('.')
            else:
                new_row.append(c)
        new_grid.append(new_row)
    return new_grid


def process(puzzle_input, minutes, verbose=False):
    grid = [list(row) for row in puzzle_input]
    if verbose:
        pprint(grid)
    seen = list()
    for minute in range(minutes):
        flat = ''.join([c for row in grid for c in row])
        if flat in seen:
            # sequence will repeat every minute - i minutes, starting at i
            i = seen.index(flat)
            i = (minutes - minute) % (minute - i) + i
            flat = seen[i]
            break
        seen.append(flat)
        grid = run_one(grid, verbose=verbose)
        if verbose:
            print('After {} minute:'.format(minute + 1))
            pprint(grid)
    else:
        flat = ''.join([c for row in grid for c in row])
    c = Counter(flat)
    return c['|'] * c['#']


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
        print('Part one: {}'.format(process(puzzle_input, 10, verbose=args.verbose)))
        print('Part two: {}'.format(process(puzzle_input, 1000000000, verbose=args.verbose)))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
