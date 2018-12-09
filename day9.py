#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 9 module."""
from __future__ import division, print_function

import re

from blist import blist


def run(first, last, circle, scores, num_players, index):
    for marble in range(first, last + 1):
        player = (marble - 1) % num_players
        if marble % 23 == 0:
            removed_index = (index - 7) % len(circle)
            removed_marble = circle.pop(removed_index)
            scores[player] += marble + removed_marble
            index = removed_index % len(circle)
            # print(marble, removed_marble)
        else:
            index = (index + 2) % len(circle)
            # Note: if you print circle for debugging purposes, it won't look
            # the same as aoc example since we insert before 0 instead of
            # appending when index is 0
            circle.insert(index, marble)
    return index


def process(line):
    m = re.match(r'(?P<num_players>\d+) (players; last marble is worth )?(?P<last_marble>\d+)', line)
    if not m:
        return (None, None)
    num_players = int(m.group('num_players'))
    last_marble = int(m.group('last_marble'))
    scores = [0 for _ in range(num_players)]

    # part one
    circle = blist([0])
    index = run(1, last_marble, circle, scores, num_players, 0)
    p1 = max(scores)
    run(last_marble + 1, last_marble * 100, circle, scores, num_players, index)
    return (p1, max(scores))


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
                p1, p2 = process(line)
                print('Part one: {}'.format(p1))
                print('Part two: {}'.format(p2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
