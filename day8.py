#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 8 module."""
from __future__ import division, print_function


def make_node(nums):
    node = {'children': [], 'metadata': []}
    num_children = nums.pop(0)
    metadata_entries = nums.pop(0)
    for child in range(num_children):
        node['children'].append(make_node(nums))
    for metadata in range(metadata_entries):
        node['metadata'].append(nums.pop(0))
    return node


def sum_metadata(node):
    n = sum(node['metadata'])
    for child in node['children']:
        n += sum_metadata(child)
    return n


def value(node):
    if node['children']:
        val = 0
        for i in node['metadata']:
            if i > 0:
                try:
                    val += value(node['children'][i - 1])
                except IndexError:
                    pass
        return val
    else:
        return sum(node['metadata'])


def process(puzzle_input):
    root = make_node([int(x) for x in puzzle_input.split()])
    return (sum_metadata(root), value(root))


def main():
    """Main entry point."""
    import argparse
    import fileinput

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input file to read ("-" for stdin)')
    args = parser.parse_args()
    try:
        for line in fileinput.input(args.infile):
            p1, p2 = process(line.strip())
            print('Part one: {}'.format(p1))
            print('Part two: {}'.format(p2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
