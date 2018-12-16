#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 16 module."""
from __future__ import division, print_function

from collections import defaultdict


def addr(regs, a, b, c):
    r = list(regs)
    r[c] = r[a] + r[b]
    return r


def addi(regs, a, b, c):
    r = list(regs)
    r[c] = r[a] + b
    return r


def mulr(regs, a, b, c):
    r = list(regs)
    r[c] = r[a] * r[b]
    return r


def muli(regs, a, b, c):
    r = list(regs)
    r[c] = r[a] * b
    return r


def banr(regs, a, b, c):
    r = list(regs)
    r[c] = r[a] & r[b]
    return r


def bani(regs, a, b, c):
    r = list(regs)
    r[c] = r[a] & b
    return r


def borr(regs, a, b, c):
    r = list(regs)
    r[c] = r[a] | r[b]
    return r


def bori(regs, a, b, c):
    r = list(regs)
    r[c] = r[a] | b
    return r


def setr(regs, a, b, c):
    r = list(regs)
    r[c] = r[a]
    return r


def seti(regs, a, b, c):
    r = list(regs)
    r[c] = a
    return r


def gtir(regs, a, b, c):
    r = list(regs)
    if a > r[b]:
        r[c] = 1
    else:
        r[c] = 0
    return r


def gtri(regs, a, b, c):
    r = list(regs)
    if r[a] > b:
        r[c] = 1
    else:
        r[c] = 0
    return r


def gtrr(regs, a, b, c):
    r = list(regs)
    if r[a] > r[b]:
        r[c] = 1
    else:
        r[c] = 0
    return r


def eqir(regs, a, b, c):
    r = list(regs)
    if a == r[b]:
        r[c] = 1
    else:
        r[c] = 0
    return r


def eqri(regs, a, b, c):
    r = list(regs)
    if r[a] == b:
        r[c] = 1
    else:
        r[c] = 0
    return r


def eqrr(regs, a, b, c):
    r = list(regs)
    if r[a] == r[b]:
        r[c] = 1
    else:
        r[c] = 0
    return r


instructions = [
    'addr',
    'addi',
    'mulr',
    'muli',
    'banr',
    'bani',
    'borr',
    'bori',
    'setr',
    'seti',
    'gtir',
    'gtri',
    'gtrr',
    'eqir',
    'eqri',
    'eqrr',
]


def process(puzzle_input, verbose=False):
    opcodes = [None for x in range(16)]
    potential_opcodes = defaultdict(set)
    p1 = 0
    for i in range(0, len(puzzle_input), 4):
        if not puzzle_input[i + 0].startswith('Before:'):
            break
        before = [int(x) for x in puzzle_input[i + 0][9:-1].split(',')]
        (opcode, a, b, c) = [int(x) for x in puzzle_input[i + 1].split()]
        after = [int(x) for x in puzzle_input[i + 2][9:-1].split(',')]
        potential = 0
        for inst in instructions:
            if after == globals()[inst](before, a, b, c):
                potential += 1
                potential_opcodes[inst].add(opcode)
        if potential >= 3:
            p1 += 1

    found = set()
    while None in opcodes:
        for inst, potential in potential_opcodes.items():
            potential.difference_update(found)
            if len(potential) == 1:
                opcode = potential.pop()
                found.add(opcode)
                opcodes[opcode] = inst
                if verbose:
                    print('{}: {}'.format(inst, opcode))

    regs = [0, 0, 0, 0]
    for line in puzzle_input[i:]:
        if not line:
            continue
        opcode, a, b, c = [int(x) for x in line.split()]
        regs = globals()[opcodes[opcode]](regs, a, b, c)

    return p1, regs[0]


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
        puzzle_input = [line.strip() for line in fileinput.input(args.infile)]
        p1, p2 = process(puzzle_input, verbose=args.verbose)
        print('Part one: {}'.format(p1))
        print('Part two: {}'.format(p2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
