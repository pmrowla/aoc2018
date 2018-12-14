#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 14 module."""
from __future__ import division, print_function


def process(puzzle_input, verbose=False):
    input_s = puzzle_input
    input_n = int(puzzle_input)
    recipes = [3, 7]
    first = 0
    second = 1

    p1 = None
    p2 = None

    while p1 is None or p2 is None:
        # Note: part 2 is real slow
        new_recipes = [int(x) for x in str(recipes[first] + recipes[second])]
        recipes.extend(new_recipes)
        first = (first + 1 + recipes[first]) % len(recipes)
        second = (second + 1 + recipes[second]) % len(recipes)
        if p1 is None and len(recipes) >= input_n + 10:
            p1 = ''.join([str(x) for x in recipes[input_n:input_n + 10]])
            print('Part one: {}'.format(p1))
        if p2 is None and len(recipes) >= len(input_s):
            try:
                i = ''.join([str(x) for x in recipes[-(len(input_s) + len(new_recipes)):]]).index(input_s)
                p2 = len(recipes) - len(input_s) - len(new_recipes) + i
                print('Part two: {}'.format(p2))
            except ValueError:
                pass

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
        for line in fileinput.input(args.infile):
            (p1, p2) = process(line.strip(), verbose=args.verbose)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
