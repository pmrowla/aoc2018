#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 22 module."""
from __future__ import division, print_function

import itertools
import re
from heapq import heappush, heappop

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


def pprint(grid):
    for row in grid:
        print(''.join([x[1] for x in row]))


def make_grid(depth, target, verbose=False):
    tx, ty = target
    grid = []
    for y in range(ty + 100):
        row = []
        for x in range(tx + 100):
            if (x, y) in [(0, 0), target]:
                geo_index = 0
            elif y == 0:
                geo_index = x * 16807
            elif x == 0:
                geo_index = y * 48271
            else:
                geo_index = row[x - 1][0] * grid[y - 1][x][0]
            erosion = (geo_index + depth) % 20183
            type_ = '.=|'[erosion % 3]
            # 2-tuple: (erosion_level, region_type)
            row.append([erosion, type_])
        grid.append(row)
    return grid


def adjacent(grid, pos, tool, target):
    x, y = pos
    type_ = grid[y][x][1]
    adj = set()
    for x1, y1 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
        if y1 >= 0 and y1 < len(grid) and x1 >= 0 and x1 < len(grid[y1]):
            adj_type = grid[y1][x1][1]
            time = 1
            if type_ == adj_type or \
                    (adj_type == '.' and tool in ('gear', 'torch')) or \
                    (adj_type == '=' and tool in ('gear', 'neither')) or \
                    (adj_type == '|' and tool in ('torch', 'neither')):
                # no equipment change
                new_tool = tool
            else:
                # need equipment change
                time += 7
                if adj_type == '.':
                    if type_ == '=':
                        new_tool = 'gear'
                    else:
                        new_tool = 'torch'
                elif adj_type == '=':
                    if type_ == '.':
                        new_tool = 'gear'
                    else:
                        new_tool = 'neither'
                else:
                    if type_ == '.':
                        new_tool = 'torch'
                    else:
                        new_tool = 'neither'
            if (x1, y1) == target and new_tool == 'gear':
                # must switch back to torch after entering target region
                time += 7
                new_tool = 'torch'
            adj.add(((x1, y1), new_tool, time))
    return adj


q = []
entries = {}
counter = itertools.count()


def add_update_prio(p, prio):
    if p in entries:
        # invalidate existing entry
        entry = entries[p]
        entry[-1] = False
    entry = [prio, next(counter), p, True]
    entries[p] = entry
    heappush(q, entry)


def pop_min_prio():
    while q:
        _, _, p, valid = heappop(q)
        if p in entries and valid:
            del entries[p]
            return p
    raise RuntimeError('empty prio q')


def dijkstra(grid, pos, target, verbose=False):
    # determine distance from pos to target
    dist = {}
    prev = {}
    add_update_prio((pos, 'torch'), 0)
    dist[(pos, 'torch')] = 0
    if tqdm:
        t = tqdm(total=len(grid) * len(grid[-1]) * 2)
    while q:
        u, tool = pop_min_prio()
        if u == target:
            break
        if t:
            t.update(1)
        for v, new_tool, time in adjacent(grid, u, tool, target):
            alt = dist[(u, tool)] + time
            if (v, new_tool) not in dist or alt < dist[(v, new_tool)]:
                dist[(v, new_tool)] = alt
                prev[(v, new_tool)] = (u, tool)
                add_update_prio((v, new_tool), alt)
    t.close()
    dist = {k: v for k, v in dist.items() if v is not None}
    prev = {k: v for k, v in prev.items() if v is not None}
    return dist, prev


def process(puzzle_input, verbose=False):
    depth = int(puzzle_input[0].split()[-1])
    tx, ty = tuple([int(x) for x in puzzle_input[1].split()[-1].split(',')])
    if verbose:
        print('depth: {} target: {}'.format(depth, (tx, ty)))
    grid = make_grid(depth, (tx, ty), verbose=verbose)
    if verbose:
        pprint(grid)
    risk_level = {'.': 0, '=': 1, '|': 2}
    p1 = sum([risk_level.get(x[1], 0) for row in grid[:ty + 1] for x in row[:tx + 1]])
    dist, prev = dijkstra(grid, (0, 0), (tx, ty), verbose=verbose)
    if verbose:
        print('reversed route:')
        p = (tx, ty)
        tool = 'torch'
        print(p, tool, dist[(p, tool)])
        p, tool = prev[(p, tool)]
        while p != (0, 0):
            print(p, tool, dist[(p, tool)])
            p, tool = prev[(p, tool)]
    return p1, dist[((tx, ty), 'torch')]


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
