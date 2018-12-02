#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 2 module."""
from __future__ import division, print_function

from collections import Counter


def hamming_distance(x, y):
    return sum(c != d for c, d in zip(x, y))


def part_one(lines):
    two = 0
    three = 0
    for line in lines:
        c = Counter(line)
        if 2 in c.values():
            two += 1
        if 3 in c.values():
            three += 1
    return two * three


def part_two(lines):
    '''Find the 2 strings in the input set with a hamming distance of 1 and
    return a string w/the single differing character removed.
    '''
    for i in range(len(lines)):
        line = lines[i].strip().lower()
        for s in lines[i:]:
            s = s.strip().lower()
            if hamming_distance(line, s) == 1:
                for j, (c, d) in enumerate(zip(line, s)):
                    if c != d:
                        return line[0:j] + line[j + 1:]
    return None


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
