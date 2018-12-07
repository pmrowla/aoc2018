#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 7 module."""
from __future__ import division, print_function

import re
from string import ascii_uppercase


def part_one(children, prereqs):
    order = []
    # top level is nodes without prerequisites
    available = set(children.keys()) - set(prereqs.keys())
    while available:
        step = sorted(available)[0]
        order.append(step)
        available.remove(step)
        if step in children:
            for x in children[step]:
                if x not in order and (x not in prereqs or not prereqs[x] - set(order)):
                    available.add(x)
    return ''.join(order)


def part_two(order, prereqs, num_workers=5, extra_duration=60):
    workers = []
    for i in range(num_workers):
        workers.append({'step': None, 'remaining': 0})
    todo = list(order)
    done = set()
    second = 0
    while len(done) < len(order):
        for w in workers:
            if w['step'] is None:
                for i in range(len(todo)):
                    step = todo[i]
                    if step not in prereqs or not prereqs[step] - done:
                        w['step'] = step
                        w['duration'] = ord(step) - ord('A') + extra_duration + 1
                        todo.pop(i)
                        break
        second += 1
        for w in workers:
            if w['step'] is not None:
                w['duration'] -= 1
                if w['duration'] == 0:
                    done.add(w['step'])
                    w['step'] = None
    return second


def process(puzzle_input):
    children = {}
    prereqs = {}
    for line in puzzle_input:
        m = re.match(r'^Step (?P<prereq>\w) must be finished before step (?P<step>\w) can begin\.$', line.strip())
        step = m.group('step')
        prereq = m.group('prereq')
        if step in prereqs:
            prereqs[step].add(prereq)
        else:
            prereqs[step] = set([prereq])
        if prereq in children:
            children[prereq].add(step)
        else:
            children[prereq] = set([step])

    order = part_one(children, prereqs)

    return (order, part_two(order, prereqs))


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
