#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 12 module."""
from __future__ import division, print_function

from enum import Enum


_directions = '^>v<'


def pprint(track, carts):
    out = []
    for y, row in enumerate(track):
        line = list(row)
        out.append(line)
    for c in carts:
        x, y = c['pos']
        if c['crashed']:
            out[y][x] = 'X'
        else:
            out[y][x] = _directions[c['dir']]
    for row in out:
        print(''.join(row))


def parse_input(puzzle_input):
    track = []
    carts = []
    for y, line in enumerate(puzzle_input):
        row = []
        for x, c in enumerate(line):
            if c in _directions:
                cart = {
                    'pos': (x, y),
                    'dir': _directions.index(c),
                    'next_turn': 0,
                    'crashed': False,
                }
                carts.append(cart)
                row.append('|-|-'[cart['dir']])
            else:
                row.append(c)
        track.append(row)
    return (track, carts)


def tick(track, carts, verbose=False):
    if verbose:
        pprint(track, carts)
    crashes = []
    carts = sorted(carts, key=lambda x: x['pos'])
    for i, cart in enumerate(carts):
        if not cart['crashed']:
            # move cart
            x, y = cart['pos']
            if cart['dir'] == 0:
                y -= 1
            elif cart['dir'] == 1:
                x += 1
            elif cart['dir'] == 2:
                y += 1
            else:
                x -= 1
            cart['pos'] = (x, y)

            # check for collision
            for j in range(len(carts)):
                if i != j and cart['pos'] == carts[j]['pos']:
                    cart['crashed'] = True
                    carts[j]['crashed'] = True
                    crashes.append((x, y))

            # check for turns
            t = track[y][x]
            if t == '/':
                if cart['dir'] in (0, 2):
                    cart['dir'] += 1
                else:
                    cart['dir'] -= 1
            elif t == '\\':
                if cart['dir'] in (1, 3):
                    cart['dir'] += 1
                else:
                    cart['dir'] -= 1
            elif t == '+':
                turns = [-1, 0, 1]
                cart['dir'] += turns[cart['next_turn']]
                cart['next_turn'] = (cart['next_turn'] + 1) % 3
            cart['dir'] %= 4
    return crashes


def process(puzzle_input, verbose=False):
    track, carts = parse_input(puzzle_input)

    crashes = []
    while len(carts) > 1:
        crashes.extend(tick(track, carts, verbose))
        carts = [c for c in carts if not c['crashed']]

    return crashes[0], carts[0]['pos']


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    parser.add_argument('-v', '--verbose', '-d', '--debug',
                        action='store_true', dest='verbose', help='verbose output')
    args = parser.parse_args()
    puzzle_input = [line.rstrip() for line in fileinput.input(args.infile)]
    try:
        (p1, p2) = process(puzzle_input, verbose=args.verbose)
        print('Part one: {}'.format(p1))
        print('Part two: {}'.format(p2))

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
