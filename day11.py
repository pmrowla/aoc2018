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


def square_power(x, y, grid, size=3):
    '''Return total power of the specified sized square w/top-left at (x,y).'''
    if x + size > len(grid) or y + size > len(grid):
        raise ValueError
    return sum([n for row in grid[y:y + size] for n in row[x:x + size]])


def column_power(x, y, grid, size):
    if x > len(grid) or y + size > len(grid):
        raise ValueError('{},{},{}'.format(x, y, size))
    return sum([row[x] for row in grid[y:y + size]])


def row_power(x, y, grid, size):
    if x + size > len(grid) or y > len(grid):
        raise ValueError('{},{},{}'.format(x, y, size))
    return sum(grid[y][x:x + size])


def part_one(grid):
    max_power = None
    max_x = None
    max_y = None
    for y in range(len(grid) - 3):
        for x in range(len(grid) - 3):
            if max_power is None:
                max_power = square_power(x, y, grid)
                max_x = x + 1
                max_y = y + 1
            else:
                p = square_power(x, y, grid)
                if p > max_power:
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
        r = tqdm(range(1, 301))
    else:
        r = range(1, 301)
    for size in r:
        if size == 3:
            continue
        cur_power = square_power(0, 0, grid, size)
        # calculating every square is slow, so as we shift our box to the next
        # point just subtract the old column/row and add the new one to
        # our current total instead of recalculating the entire square.
        #
        # Note: this is still kind of slow? ~2 min on my machine for my input
        for y in range(len(grid) - size):
            for x in range(len(grid) - size):
                if x == 0:
                    if y == 0:
                        cur_power = square_power(0, 0, grid, size)
                        if cur_power > max_power:
                            max_power = cur_power
                            max_x = x + 1
                            max_y = y + 1
                            max_size = size
                    row_sav = cur_power
                else:
                    if cur_power > max_power:
                        max_power = cur_power
                        max_x = x + 1
                        max_y = y + 1
                        max_size = size
                if x + size < len(grid):
                    cur_power -= column_power(x, y, grid, size)
                    cur_power += column_power(x + size, y, grid, size)
            if y + size < len(grid):
                cur_power = row_sav
                cur_power -= row_power(0, y, grid, size)
                cur_power += row_power(0, y + size, grid, size)
                if cur_power > max_power:
                    max_power = cur_power
                    max_x = x + 1
                    max_y = y + 1
                    max_size = size
    return max_x, max_y, max_size



def process(serial_number):
    grid = []
    for y in range(1, 301):
        row = []
        for x in range(1, 301):
            row.append(power_level(x, y, serial_number))
        grid.append(row)
    p1_x, p1_y, p1_power = part_one(grid)
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
