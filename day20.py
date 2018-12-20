#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 20 module."""
from __future__ import division, print_function

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


def pprint(grid):
    [print(row) for row in grid]


def make_grid(pattern, verbose=False):
    pattern = pattern.lstrip('^').rstrip('$').upper()
    x = 0
    y = 0
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    area = {(0, 0): '.'}
    sav_pos = []
    for c in pattern:
        if c == 'N':
            area[(x, y - 1)] = '|'
            area[(x, y - 2)] = '.'
            y -= 2
        elif c == 'S':
            area[(x, y + 1)] = '|'
            area[(x, y + 2)] = '.'
            y += 2
        elif c == 'E':
            area[(x + 1, y)] = '|'
            area[(x + 2, y)] = '.'
            x += 2
        elif c == 'W':
            area[(x - 1, y)] = '|'
            area[(x - 2, y)] = '.'
            x -= 2
        elif c == '(':
            sav_pos.append((x, y))
        elif c == '|':
            x, y = sav_pos[-1]
        elif c == ')':
            x, y = sav_pos.pop()
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)
    grid = []
    # account for outer walls
    min_x -= 1
    max_x += 1
    min_y -= 1
    max_y += 1
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if x == 0 and y == 0:
                row.append('X')
            elif (x, y) in area:
                row.append(area[(x, y)])
            else:
                row.append('#')
        grid.append(''.join(row))
    return grid, (abs(min_x), abs(min_y))


def adjacent(grid, pos):
    x, y = pos
    adj = set()
    for x1, y1, x2, y2 in [(x + 1, y, x + 2, y), (x - 1, y, x - 2, y), (x, y + 1, x, y + 2), (x, y - 1, x, y - 2)]:
        try:
            if grid[y1][x1] == '|':
                adj.add((x2, y2))
        except IndexError:
            pass
    return adj


def dijkstra(grid, pos=(0, 0), verbose=False):
    # determine distance from pos to every (reachable) room in grid
    # same as routes() from day15
    dist = {}
    prev = {}
    q = set()
    q.add(pos)
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == '.':
                dist[(x, y)] = None
                prev[(x, y)] = None
                q.add((x, y))
    dist[pos] = 0
    if tqdm:
        t = tqdm(total=len(q))
    while q:
        min_p = None
        min_d = None
        u = None
        for p in dist:
            if p in q and dist[p] is not None:
                if min_p is None:
                    min_p = p
                    min_d = dist[p]
                elif dist[p] < min_d:
                    min_p = p
                    min_d = dist[p]
        if min_p is None or min_d is None:
            # remaining points in q unreachable
            break
        u = min_p
        q.remove(u)
        if t:
            t.update(1)
        for v in adjacent(grid, u):
            if v in q:
                alt = dist[u] + 1
                if dist[v] is None or alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
    t.close()
    dist = {k: v for k, v in dist.items() if v is not None}
    prev = {k: v for k, v in prev.items() if v is not None}
    return dist, prev


def process(puzzle_input, verbose=False):
    grid, origin = make_grid(puzzle_input, verbose=verbose)
    if verbose:
        pprint(grid)
    dist, prev = dijkstra(grid, pos=origin)
    paths = sorted([(k, v) for k, v in dist.items()], key=lambda x: x[1])
    return paths[-1][1], sum([doors >= 1000 for _, doors in paths])


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
            p1, p2 = process(line.strip(), verbose=args.verbose)
            print('Part one: {}'.format(p1))
            print('Part two: {}'.format(p2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
