#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 21 module."""
from __future__ import division, print_function


def valid_inputs():
    '''Determine the possible values for r0 which will cause the program to exit.'''
    # the input program is as follows:
    # # 00
    # r3 = 123
    # # 01
    # while True:
    #     r3 &= 456
    #     if r3 != 72:
    #         # goto 01 (causes infinite loop)
    #         # continue
    valid = list()
    r3 = 0
    while True:
        # 06
        r4 = r3 | 65536
        r3 = 10649702
        while True:
            # 08
            r3 += r4 & 255
            r3 &= 16777215
            r3 *= 65899
            r3 &= 16777215
            if 256 > r4:
                # 28
                # r5 = r3 == r0
                # if r3 == r0: exit
                # print(r3)
                # if r3 != 10504829:
                #     raise Exception('r3 != 10504829')
                if r3 not in valid:
                    valid.append(r3)
                else:
                    return valid
                # goto 06
                break
            # r5 = 0
            # while True:
            #     # 18
            #     if (r5 + 1) * 256 > r4:
            #         # 26
            #         r4 = r5
            #         # goto 08
            #         break
            #     r5 += 1
            #     # goto 18
            r4 = r4 // 256


def process(puzzle_input, r0=0, verbose=False):
    if not puzzle_input[0].startswith('#ip'):
        raise ValueError('Unexpected input format, missing #ip line')
    ip_reg = int(puzzle_input[0].split()[1])
    valid = valid_inputs()
    # if verbose:
    #     print(valid)
    return valid[0], valid[-1]


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
        p1,p2 = process(puzzle_input, verbose=args.verbose)
        print('Part one: {}'.format(p1))
        print('Part two: {}'.format(p2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
