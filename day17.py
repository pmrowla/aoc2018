#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 17 module."""
from __future__ import division, print_function

import re


def make_grid(puzzle_input, verbose=False):
    clay = []
    min_x = 500
    max_x = 500
    min_y = None
    max_y = None
    for line in puzzle_input:
        m = re.match(r'(?P<c>\w)=(?P<x>\d+), \w=(?P<y1>\d+)\.\.(?P<y2>\d+)', line)
        if m:
            if m.group('c') == 'x':
                x1 = int(m.group('x'))
                x2 = int(m.group('x'))
                y1 = int(m.group('y1'))
                y2 = int(m.group('y2'))
            else:
                x1 = int(m.group('y1'))
                x2 = int(m.group('y2'))
                y1 = int(m.group('x'))
                y2 = int(m.group('x'))
            clay.append((x1, x2, y1, y2))
            min_x = min(min_x, x1, x2)
            max_x = max(max_x, x1, x2)
            if min_y is None:
                min_y = min(y1, y2)
            else:
                min_y = min(min_y, y1, y2)
            if max_y is None:
                max_y = max(y1, y2)
            else:
                max_y = max(max_y, y1, y2)
    min_x -= 1
    max_x += 1
    grid = []
    for x in range(max_y + 1):
        row = list(['.'] * (max_x - min_x + 1))
        grid.append(row)
    grid[0][500 - min_x] = '+'
    for x1, x2, y1, y2 in clay:
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                grid[y][x - min_x] = '#'
    return grid, min_x, max_x, min_y, max_y


def flow(grid, min_x, max_x, min_y, max_y, source, verbose=False):
    can_continue = False
    (x, y) = source
    if grid[y][x] == '~':
        return False
    # flow downwards as far as possible
    while grid[y + 1][x] in '.|':
        y += 1
        if grid[y][x] == '.':
            grid[y][x] = '|'
        if y == max_y:
            # we've reached end of the board
            return False
    # flow left as far as possible:
    left = None
    left_flow = True
    while x > 0:
        if grid[y][x] == '#':
            x += 1
            left = x
            left_flow = False
            break
        elif grid[y][x] == '.':
            grid[y][x] = '|'
        if grid[y + 1][x] in '~#':
            x -= 1
        else:
            break
    if left_flow and grid[y + 1][x] in '.|':
        while flow(grid, min_x, max_x, min_y, max_y, (x, y), verbose):
            pass
        x += 1
    # flow right as far as possible
    right_flow = True
    while x < max_x - min_x + 1:
        if grid[y][x] == '#':
            x -= 1
            right_flow = False
            if left:
                # this level will settle
                for x in range(left, x + 1):
                    grid[y][x] = '~'
                (x, y) = source
                if grid[y][x] == '~':
                    return False
                else:
                    return True
            break
        elif grid[y][x] == '.':
            grid[y][x] = '|'
        if grid[y + 1][x] in '~#':
            x += 1
        else:
            break
    if right_flow and grid[y + 1][x] in '.|':
        return flow(grid, min_x, max_x, min_y, max_y, (x, y), verbose)
    return False
    return left_flow or right_flow


def pprint(grid, min_x, max_x, min_y, max_y):
    print('x range: {} - {}'.format(min_x, max_x))
    for y in range(max_y + 1):
        print('{:0{width}} {}'.format(y, ''.join(grid[y]), width=len(str(max_y))))


def process(puzzle_input, verbose=False):
    grid, min_x, max_x, min_y, max_y = make_grid(puzzle_input)
    false_count = 0
    while false_count < 2:
        if not flow(grid, min_x, max_x, min_y, max_y, (500 - min_x, 0)):
            false_count += 1
        else:
            false_count = 0
    if verbose:
        pprint(grid, min_x, max_x, min_y, max_y)
    # with open('tmp.txt', 'w') as f:
    #     for y in range(max_y + 1):
    #         f.write('{:0{width}} {}\n'.format(y, ''.join(grid[y]), width=len(str(max_y))))
    p1 = sum([x in '|~' for row in grid[min_y:max_y + 1] for x in row])
    p2 = sum([x == '~' for row in grid[min_y:max_y + 1] for x in row])
    return p1, p2


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
