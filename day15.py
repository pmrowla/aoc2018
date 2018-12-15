#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 15 module."""
from __future__ import division, print_function


class ErrorElfDied(Exception):
    pass


class Wall(object):
    pass


class Unit(object):

    abbr = 'U'

    def __init__(self, x, y, atk=3):
        self.pos = (x, y)
        self.atk = atk
        self.hp = 200
        self.need_routes = True

    def __lt__(self, other):
        if self.pos[1] < other.pos[1]:
            return True
        elif self.pos[1] == other.pos[1]:
            return self.pos[0] < other.pos[0]
        return False

    def __str__(self):
        return '{}{}'.format(self.abbr, self.pos, self.hp)

    def attack(self, grid, targets, verbose=False):
        # attack adjacent enemy if possible
        neighbors = grid.neighbors(self.pos)
        potential_targets = set()
        for t in targets:
            if t.pos in neighbors:
                potential_targets.add(t)

        if potential_targets:
            t = sorted(potential_targets, key=lambda x: (x.hp, x))[0]
            t.hp -= self.atk
            return t
        return None

    def move(self, grid, targets, verbose=False):
        # move if possible
        if self.need_routes:
            # if no one else has moved or died we don't need to recompute route
            potential_moves = set()

            for t in targets:
                [potential_moves.add(p) for p in grid.reachable_neighbors(t.pos)]

            # move to nearest enemy
            self.dist, self.prev = grid.routes(self.pos, potential_moves)
            moves = []
            for m in sorted(potential_moves, key=lambda x: (x[1], x[0])):
                if m in self.dist:
                    moves.append((self.dist[m], m))
            if not moves:
                return False
            _, self.dest = sorted(moves, key=lambda x: x[0])[0]
            self.need_routes = False
        new_p = self.dest
        while self.prev[new_p] != self.pos:
            new_p = self.prev[new_p]
        if grid.distance(self.pos, new_p) != 1:
            raise Exception('move not = 1???')
        self.pos = new_p
        return True


class Elf(Unit):

    abbr = 'E'


class Goblin(Unit):

    abbr = 'G'


class Grid(object):

    @property
    def _units(self):
        return sorted(self.elves + self.goblins)

    def __init__(self, puzzle_input, elf_atk=3, verbose=False):
        self.result = None
        self._grid = []
        self.elves = []
        self.goblins = []
        self._verbose = verbose
        self.elf_atk=elf_atk
        for y, line in enumerate(puzzle_input):
            row = []
            for x, c in enumerate(line):
                if c == '#':
                    row.append(Wall())
                else:
                    if c == 'E':
                        elf = Elf(x, y, atk=elf_atk)
                        self.elves.append(elf)
                        row.append(elf)
                    elif c == 'G':
                        goblin = Goblin(x, y)
                        self.goblins.append(goblin)
                        row.append(goblin)
                    else:
                        row.append(None)
            self._grid.append(row)

    def finish(self):
        print('Combat ends after {} full rounds'.format(self.completed_rounds))
        if not self.elves:
            self.result = sum([g.hp for g in self.goblins])
            print('Goblins win with {} hp remaining'.format(self.result))
        else:
            self.result = sum([e.hp for e in self.elves])
            print('Elves win with {} hp remaining'.format(self.result))

    def _update(self):
        for row in self._grid:
            for i, x in enumerate(row):
                if x and not isinstance(x, Wall):
                    row[i] = None
        for u in self._units:
            if u.hp > 0:
                self._grid[u.pos.y][u.pos.x] = u

    def pprint(self):
        for row in self._grid:
            line = []
            units = []
            for x in row:
                if isinstance(x, Wall):
                    line.append('#')
                elif isinstance(x, Unit) and x.hp > 0:
                    line.append(x.abbr)
                    units.append(x)
                else:
                    line.append('.')
            line.append('  ')
            line.append(', '.join(['{}({})'.format(x.abbr, x.hp) for x in units]))
            print(''.join(line))

    def reachable(self, pos):
        '''Return True if pos is a reachable location.'''
        x, y = pos
        try:
            return self._grid[y][x] is None
        except IndexError:
            return False

    def reachable_neighbors(self, pos):
        return set([p for p in self.neighbors(pos) if self.reachable(p)])

    def neighbors(self, pos):
        x, y = pos
        return set([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    def distance(self, p1, p2):
        '''Return the manhattan distance between two points.'''
        return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

    def routes(self, pos, search):
        '''Get routes from pos to the given points.'''
        search = set(search)
        dist = {}
        prev = {}
        q = set()
        q.add(pos)
        for y, row in enumerate(self._grid):
            for x, c in enumerate(row):
                if c is None:
                    dist[(x, y)] = None
                    prev[(x, y)] = None
                    q.add((x, y))
        dist[pos] = 0
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
            if u in search:
                search.remove(u)
            if not search:
                break
            for v in self.reachable_neighbors(u):
                if v in q:
                    alt = dist[u] + 1
                    if dist[v] is None or alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
        dist = {k: v for k, v in dist.items() if v is not None}
        prev = {k: v for k, v in prev.items() if v is not None}
        return dist, prev

    def run(self, p2=False):
        self.completed_rounds = 0
        while True:
            for u in list(self._units):
                if u.hp > 0:
                    if isinstance(u, Elf):
                        targets = self.goblins
                    else:
                        targets = self.elves
                    if not targets:
                        return self.finish()
                    t = u.attack(self, targets, verbose=self._verbose)
                    if t:
                        if t.hp <= 0:
                            if isinstance(t, Elf):
                                if p2:
                                    raise ErrorElfDied
                                self.elves.remove(t)
                            else:
                                self.goblins.remove(t)
                            x, y = t.pos
                            self._grid[y][x] = None
                            for x in self._units:
                                x.need_routes = True
                    else:
                        orig_x, orig_y = u.pos
                        if u.move(self, targets, verbose=self._verbose):
                            x, y = u.pos
                            self._grid[orig_y][orig_x] = None
                            self._grid[y][x] = u
                            for x in self._units:
                                if x is not u:
                                    x.need_routes = True
                        t = u.attack(self, targets, verbose=self._verbose)
                        if t:
                            if t.hp <= 0:
                                if isinstance(t, Elf):
                                    if p2:
                                        raise ErrorElfDied
                                    self.elves.remove(t)
                                else:
                                    self.goblins.remove(t)
                                x, y = t.pos
                                self._grid[y][x] = None
                                for x in self._units:
                                    x.need_routes = True
            self.completed_rounds += 1
            if self._verbose:
                print('After {} (elf_atk: {}):'.format(self.completed_rounds, self.elf_atk))
                self.pprint()


def part_one(puzzle_input, verbose=False):
    grid = None
    grid = Grid(puzzle_input, verbose=verbose)
    if verbose:
        grid.pprint()
    grid.run()
    return grid.completed_rounds * grid.result


def part_two(puzzle_input, verbose=False):
    p2 = None
    elf_atk = 3
    while True:
        elf_atk += 1
        grid = Grid(puzzle_input, elf_atk=elf_atk, verbose=verbose)
        try:
            grid.run(p2=True)
            return grid.completed_rounds * grid.result
        except ErrorElfDied:
            continue


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
        p1 = part_one(puzzle_input, verbose=args.verbose)
        p2 = part_two(puzzle_input, verbose=args.verbose)
        print('Part one: {}'.format(p1))
        print('Part two: {}'.format(p2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
