#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 12 module."""
from __future__ import division, print_function

import re


def process(puzzle_input, generations=20):
    m = re.match(r'initial state: (?P<state>[.#]+)', puzzle_input[0])
    if not m:
        return
    state = ''.join(['...', m.group('state').rstrip('.'), '...'])
    zero_index = 3
    rules = {}
    for line in puzzle_input[1:]:
        m = re.match(r'(?P<pattern>[.#]{5}) => (?P<next>[.#])', line)
        if m:
            rules[m.group('pattern')] = m.group('next')
    last = ''
    for gen in range(generations):
        if state.strip('.') == last:
            # after some number of generations, each subsequent generation is
            # the same as the prior gen shifted to the right by one.
            #
            # would probably be better to programatically determine the shift
            # amount, but at least for my aoc input it's 1
            result = 0
            for i, x in enumerate(state):
                if x == '#':
                    result += i - zero_index + generations - gen
            return result
        last = state.strip('.')
        next_state = ['..']
        for i in range(2, len(state) - 2):
            try:
                next_state.append(rules[state[i - 2:i + 3]])
            except KeyError:
                next_state.append('.')
        if next_state[1] == '#':
            next_state.insert(0, '.')
            zero_index += 1
        state = ''.join(next_state).rstrip('.') + '...'

    result = 0
    for i, x in enumerate(state):
        if x == '#':
            result += i - zero_index
    return result


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    args = parser.parse_args()
    puzzle_input = [line.strip() for line in fileinput.input(args.infile)]
    try:
        print('Part one: {}'.format(process(puzzle_input)))
        print('Part two: {}'.format(process(puzzle_input, generations=50000000000)))

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
