#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 24 module."""
from __future__ import division, print_function

import re

from copy import deepcopy
from itertools import count

try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


class UnitGroup(object):

    def __init__(self, name, units, hp, atk, dmg, init, weak, immune):
        #
        self.name = name
        # unit count
        self.units = units
        # hp per unit
        self.hp = hp
        # atk damage
        self.atk = atk
        # damage type
        self.dmg = dmg
        # initiative
        self.init = init
        # weaknesses
        self.weak = set(weak)
        # immunities
        self.immune = set(immune)

        self.target = None

    @property
    def power(self):
        return self.units * self.atk

    @property
    def alive(self):
        return self.units > 0

    def __str__(self):
        return '{}: {} units {} hp (weak to {}; immune to {}) atk {} {} init {}'.format(self.name, self.units, self.hp, self.weak, self.immune, self.atk, self.dmg, self.init)

    def __lt__(self, other):
        if self.power < other.power:
            return True
        elif self.power == other.power:
            return self.init < other.init
        return False

    def atk_damage(self, t):
        if not self.alive or self.dmg in t.immune:
            return 0
        elif self.dmg in t.weak:
            return self.power * 2
        else:
            return self.power

    def select_target(self, targets, verbose=False):
        '''Select a target and remove it from the list of potential targets.'''
        self.target = None
        if self.alive and targets:
            potential = sorted([(self.atk_damage(t), t) for t in targets])
            if potential[-1][0] > 0:
                self.target = potential[-1][1]
                targets.remove(self.target)
                if verbose:
                    print('{} would deal {} {} damage'.format(self.name, self.target.name, potential[-1][0]))
        return self.target

    def take_damage(self, damage):
        if self.alive:
            killed = damage // self.hp
            killed = min(killed, self.units)
            self.units -= killed
        else:
            killed = 0
        return killed

    def attack(self, verbose=False):
        killed = 0
        if self.alive and self.target:
            killed = self.target.take_damage(self.atk_damage(self.target))
            if verbose:
                print('{} attacks {}, killing {} units'.format(self.name, self.target.name, killed))
        return killed


def parse_groups(puzzle_input, verbose=False):
    immune_system = []
    infection = []
    for line in puzzle_input:
        if not line:
            continue
        elif line.startswith('Immune'):
            g = immune_system
            name = 'Immune group'
            c = count(start=1)
            continue
        elif line.startswith('Infection'):
            g = infection
            name = 'Infection group'
            c = count(start=1)
            continue
        m = re.match(
            r'^(?P<units>\d+) units each with (?P<hp>\d+) hit points ' \
            r'(\(((weak to (?P<weak>(\w+(, )?)+)|immune to (?P<immune>(\w+(, )?)+))(; )?){1,2}\) )?' \
            r'with an attack that does (?P<atk>\d+) (?P<dmg>\w+) damage at initiative (?P<init>\d+)$',
            line)
        if m:
            if m.group('weak'):
                weak = [x.strip() for x in m.group('weak').split(',')]
            else:
                weak = []
            if m.group('immune'):
                immune = [x.strip() for x in m.group('immune').split(',')]
            else:
                immune = []
            g.append(UnitGroup(
                '{} {}'.format(name, next(c)),
                int(m.group('units')),
                int(m.group('hp')),
                int(m.group('atk')),
                m.group('dmg'),
                int(m.group('init')),
                weak,
                immune,
            ))
        else:
            raise Exception('Could not parse line: {}'.format(line))
    if verbose:
        print('Immune system:')
        [print(x) for x in immune_system]
        print('Infection:')
        [print(x) for x in infection]
        print()
    return immune_system, infection


def run(immune_system, infection, boost=0, verbose=False):
    immune_system = deepcopy(immune_system)
    infection = deepcopy(infection)
    if boost:
        for u in immune_system:
            u.atk += boost
    if verbose:
        print('Immune system:')
        [print(x) for x in immune_system]
        print('Infection:')
        [print(x) for x in infection]
        print()
    while immune_system and infection:
        # target selection
        inf_targets = set(infection)
        imm_targets = set(immune_system)
        for u in sorted(infection, key=lambda x: (x.power, x.init), reverse=True):
            u.select_target(imm_targets, verbose=verbose)
        for u in sorted(immune_system, key=lambda x: (x.power, x.init), reverse=True):
            u.select_target(inf_targets, verbose=verbose)
        if verbose:
            print()

        # attack
        killed = 0
        for u in sorted(immune_system + infection, key=lambda x: x.init, reverse=True):
            killed += u.attack(verbose=verbose)
        if verbose:
            print()
        if killed == 0:
            raise RuntimeError('Infinite loop, no remaining units can be killed')

        immune_system = [u for u in immune_system if u.alive]
        infection = [u for u in infection if u.alive]
        if verbose:
            print('Immune system:')
            [print(x) for x in immune_system]
            print('Infection:')
            [print(x) for x in infection]
            print()
    return immune_system, infection


def process(puzzle_input, verbose=False):
    immune_system, infection = parse_groups(puzzle_input, verbose=verbose)
    boost = 0
    p1 = None
    if tqdm:
        t = tqdm(total=100)
    while True:
        try:
            imm, inf = run(immune_system, infection, boost=boost, verbose=verbose)
            if boost == 0:
                if imm:
                    p1 = sum([u.units for u in imm])
                else:
                    p1 = sum([u.units for u in inf])
            if imm:
                break
        except RuntimeError:
            pass
        boost += 1
        if t:
            t.update(1)
    if t:
        t.update(100 - boost)
        t.close()
    return p1, sum([u.units for u in imm])


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
