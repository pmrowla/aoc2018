#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 3 module."""
from __future__ import division, print_function

import re


def parse_line(line):
    m = re.match('^#(?P<id>\d+)\s+@\s+(?P<x>\d+),(?P<y>\d+):\s+(?P<width>\d+)x(?P<height>\d+)$', line.strip())
    claim = {}
    gdict = m.groupdict()
    for k in gdict:
        claim[k] = int(gdict[k])
    return claim

def part_one(puzzle_input):
    grid = list()
    for i in range(1000):
        grid.append([0] * 1000)

    for line in puzzle_input:
        claim = parse_line(line)
        x = claim['x']
        y = claim['y']
        for i in range(claim['height']):
            for j in range(claim['width']):
                grid[y + i][x + j] += 1
    return sum([(square > 1) for line in grid for square in line])


def part_two(puzzle_input):
    grid = list()
    for i in range(1000):
        line = list()
        for j in range(1000):
            line.append(set())
        grid.append(line)

    claims = set()
    for line in puzzle_input:
        claim = parse_line(line)
        claims.add(claim['id'])
        x = claim['x']
        y = claim['y']
        for i in range(claim['height']):
            for j in range(claim['width']):
                grid[y + i][x + j].add(claim['id'])
    overlaps = set()
    for line in grid:
        for square in line:
            if len(square) > 1:
                for claim in square:
                    overlaps.add(claim)
    return claims - overlaps


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    args = parser.parse_args()
    try:
        puzzle_input = list(fileinput.input(args.infile))
        print('Part one: {}'.format(part_one(puzzle_input)))
        print('Part two: {}'.format(part_two(puzzle_input)))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
