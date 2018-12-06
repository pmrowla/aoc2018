#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 6 module."""
from __future__ import division, print_function

from collections import Counter


def process(puzzle_input):
    coords = []
    left = 0
    right = 0
    top = 0
    bottom = 0
    for line in puzzle_input:
        c = line.strip().split(', ')
        x = int(c[0])
        y = int(c[1])
        left = min(x, left)
        right = max(x, right)
        top = min(y, top)
        bottom = max(y, bottom)
        coords.append((x, y))
    infinite = set()

    p2 = 0
    grid = []
    for y in range(top, bottom + 1):
        row = []
        for x in range(left, right + 1):
            distances = sorted([(i, abs(cx - x) + abs(cy - y)) for i, (cx, cy) in enumerate(coords)],
                               key=lambda x: x[1])
            c = -1
            if distances[0][1] != distances[1][1]:
                c = distances[0][0]
                # area is infinite if it touches bounding box
                if x in (left, right) or y in (top, bottom):
                    infinite.add(c)
            row.append(c)

            if sum(dist for i, dist in distances) < 10000:
                p2 += 1
        grid.append(row)

    p1 = Counter([c for row in grid for c in row if c not in infinite]).most_common(1)[0][1]

    return (p1, p2)


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    args = parser.parse_args()
    try:
        p1, p2 = process(fileinput.input(args.infile))
        print('Part one: {}'.format(p1))
        print('Part two: {}'.format(p2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
