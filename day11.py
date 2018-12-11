#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 11 module."""
from __future__ import division, print_function

import re
from blist import blist

try:
    from tqdm import tqdm
    _has_tqdm = True
except ImportError:
    _has_tqdm = False


def power_level(x, y, serial_number):
    '''Return the power level for the specified fuel cell.'''
    rack_id = x + 10
    return ((rack_id * y + serial_number) * rack_id) // 100 % 10 - 5


def area(x, y, grid, size):
    '''Return the area of the given square.'''
    return grid[y + size][x + size] + grid[y][x] - grid[y][x + size] - grid[y + size][x]


def max_square(grid, size):
    '''Return the maximum power square of specified size.'''
    max_power = None
    max_x = None
    max_y = None
    for y in range(len(grid) - size):
        for x in range(len(grid) - size):
            p = area(x, y, grid, size)
            if max_power is None or p > max_power:
                max_power = p
                max_x = x + 1
                max_y = y + 1
    return max_x, max_y, max_power


def part_two(grid, p1_x, p1_y, p1_power):
    max_power = p1_power
    max_x = p1_x
    max_y = p1_y
    max_size = 3
    if _has_tqdm:
        r = tqdm(range(2, 301))
    else:
        r = range(2, 301)
    for size in r:
        if size == 3:
            continue
        x, y, power = max_square(grid, size)
        if power > max_power:
            max_power = power
            max_x = x
            max_y = y
            max_size = size
    return max_x, max_y, max_size


def process(serial_number):
    grid = []
    for y in range(301):
        row = []
        for x in range(301):
            # generate grid as summed area table
            p = power_level(x, y, serial_number)
            if y > 0:
                p += grid[y - 1][x]
                if x > 0:
                    p -= grid[y - 1][x - 1]
            if x > 0:
                p += row[x - 1]
            row.append(p)
        grid.append(row)
    p1_x, p1_y, p1_power = max_square(grid, 3)
    p2_x, p2_y, p2_size = part_two(grid, p1_x, p1_y, p1_power)
    print('Part one: {},{}'.format(p1_x, p1_y))
    print('Part two: {},{},{}'.format(p2_x, p2_y, p2_size))


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    args = parser.parse_args()
    try:
        for line in fileinput.input(args.infile):
            line = line.strip()
            if line:
                process(int(line))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
