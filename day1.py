#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 1 module."""
from __future__ import division, print_function

from itertools import cycle


def part_two(digits):
    seen = set([0])
    current = 0
    for x in cycle(digits):
        current += x
        if current in seen:
            return current
        seen.add(current)


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    args = parser.parse_args()
    try:
        puzzle_input = []
        for line in fileinput.input(args.infile):
            puzzle_input += [int(x) for x in line.split()]
        print('Part one: {}'.format(sum(puzzle_input)))
        print('Part two: {}'.format(part_two(puzzle_input)))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
