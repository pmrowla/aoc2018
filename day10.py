#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 10 module."""
from __future__ import division, print_function

import re


def distance(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def should_draw(points):
    '''Return True if the delta between min and max y values for all points is
    roughly the height of a character.
    '''
    min_y = points[0][1]
    max_y = points[0][1]
    for p in points[1:]:
        min_y = min(min_y, p[1])
        max_y = max(max_y, p[1])
    if max_y - min_y < 10:
        return True
    return False


def process(puzzle_input):
    points = []
    velocities = []
    for line in puzzle_input:
        m = re.match(r'^position=<(?P<p>\s*-?\d+,\s*-?\d+)> velocity=<(?P<v>\s*-?\d+,\s*-?\d+)>', line)
        if not m:
            continue
        p = [int(n.strip()) for n in m.group('p').split(',')]
        v = [int(n.strip()) for n in m.group('v').split(',')]
        points.append(p)
        velocities.append(v)

    sec = 0
    while True:
        if should_draw(points):
            max_x = points[0][0]
            min_x = points[0][0]
            max_y = points[0][1]
            min_y = points[0][1]
            for p in points[1:]:
                max_x = max(max_x, p[0])
                min_x = min(min_x, p[0])
                max_y = max(max_y, p[1])
                min_y = min(min_y, p[1])
            print('Part one:')
            for y in range(min_y, max_y + 1):
                line = []
                for x in range(min_x, max_x + 1):
                    if [x, y] in points:
                        line.append('#')
                    else:
                        line.append('.')
                print(''.join(line))
            print('Part two: {}'.format(sec))
            return
        for i in range(len(points)):
            points[i][0] += velocities[i][0]
            points[i][1] += velocities[i][1]
        sec += 1


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    args = parser.parse_args()
    try:
        puzzle_input = [line.strip() for line in fileinput.input(args.infile)]
        process(puzzle_input)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
