#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 19 module."""
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


def program(r2):
    # the input program is as follows:
    #
    # r1 = 0
    # r2 = 0
    # r4 = 0
    # if r0 == 0:
    #     r2 = 1018
    # elif r0 == 1:
    #     r2 = 10551418
    #     r0 = 0
    # # 1:
    # r1 = 1
    # # 2:
    # while True:
    #     r4 = 1
    #     # 3:
    #     while True:
    #         if r2 == (r1 * r4):
    #             r0 += r1
    #         r4 += 1
    #         if r4 > r2:
    #             break
    #     r1 += 1
    #     if r1 > r2:
    #         return r0
    #
    # this can be optimized to the following code
    #
    # Note: my input uses r2 for the loop range, but that may vary
    # depending on your input
    r0 = 0
    for i in range(1, r2 + 1):
        if (r2 % i) == 0:
            r0 += i
    return r0


def process(puzzle_input, regs=[0, 0, 0, 0, 0, 0], verbose=False):
    if not puzzle_input[0].startswith('#ip'):
        raise ValueError('Unexpected input format, missing #ip line')
    ip_reg = int(puzzle_input[0].split()[1])
    prog = puzzle_input[1:]
    while regs[ip_reg] >= 0 and regs[ip_reg] < len(prog):
        ip = regs[ip_reg]
        if verbose:
            print('ip={:02} {}'.format(ip, regs))
        if ip == 1:
            # See comments for program(), once we know the initial value for r2
            # just run optimized version of the program instead of simulating
            # the cpu
            return program(regs[2])
        inst, a, b, c = prog[ip].split()[0:4]
        regs = globals()[inst](regs, int(a), int(b), int(c))
        if verbose:
            print('  {} {} {} {} {}'.format(inst, a, b, c, regs))
        regs[ip_reg] += 1
    return regs[0]


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
        print('Part one: {}'.format(process(puzzle_input, verbose=args.verbose)))
        print('Part two: {}'.format(process(puzzle_input, regs=[1, 0, 0, 0, 0, 0], verbose=args.verbose)))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
