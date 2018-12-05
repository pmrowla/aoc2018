#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 5 module."""
from __future__ import division, print_function

from string import ascii_lowercase


def react(polymer, unit=None):
    '''Scan list and remove adjacent elements (in place).

    If unit is specified, any elements matching that unit will be removed.

    Returns:
        True if the list was modified.
        False if the list was not modified.
    '''
    modified = False
    i = 0
    while i < len(polymer) - 1:
        if unit and polymer[i].lower() == unit:
            polymer.pop(i)
            modified = True
        elif polymer[i] != polymer[i + 1] and \
                polymer[i].lower() == polymer[i + 1].lower():
            polymer.pop(i + 1)
            polymer.pop(i)
            modified = True
        else:
            i += 1
    return modified


def part_one(puzzle_input):
    polymer = list(puzzle_input)
    while react(polymer):
        pass
    return len(polymer)


def part_two(puzzle_input):
    # Note: this is slow (aoc input takes ~1.5min on my machine)
    lengths = []
    for c in ascii_lowercase:
        polymer = list(puzzle_input)
        while react(polymer, unit=c):
            pass
        lengths.append(len(polymer))
    return min(lengths)


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    args = parser.parse_args()
    try:
        for line in fileinput.input(args.infile):
            print('Part one: {}'.format(part_one(line.strip())))
            print('Part two: {}'.format(part_two(line.strip())))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
