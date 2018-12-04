#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Advent of Code 2018 day 4 module."""
from __future__ import division, print_function

from datetime import datetime
import re


def parse_line(line):
    '''Parse a log line into a tuple of (timestamp, event string).'''
    m = re.match(r'^\[(?P<timestamp>.+)\] (?P<event>.*)$', line.strip())
    if m:
        timestamp = datetime.strptime(m.group('timestamp'), '%Y-%m-%d %H:%M')
        return (timestamp, m.group('event'))
    return (None, None)


def start_shift(m, timestamp, state):
    # Close the previous guard's shift if needed (sleep through 1AM)
    # but I don't think this ever actually happens in aoc input?
    if state['sleep_start'] is not None:
        wake(m, None, state)

    guard_id = int(m.group('id'))
    if guard_id not in state['guards']:
        state['guards'][guard_id] = list([0] * 60)
    state['cur_guard'] = guard_id


def sleep(m, timestamp, state):
    # Note: Shifts can start prior to midnight, but my aoc input does not have
    # any cases where sleep state also starts before midnight,
    # so I don't account for that here
    state['sleep_start'] = timestamp


def wake(m, timestamp, state):
    # Note: aoc input does not include cases where the wake up event happens
    # past 1AM so I don't account for that here
    start = state['sleep_start']
    if timestamp is None:
        end = 60
    else:
        end = timestamp.minute
    for i in range(start.minute, end):
        state['guards'][state['cur_guard']][i] += 1
    state['sleep_start'] = None


def handle_events(events):
    '''Return a dict mapping guard IDs to a list w/len 60 where each element
    corresponds to total minutes slept at that minute (00-59).
    '''
    state = {
        'guards': {},
        'cur_guard': None,
        'sleep_start': None
    }
    event_patterns = {
        r'^Guard #(?P<id>\d+) begins shift$': start_shift,
        r'^falls asleep$': sleep,
        r'^wakes up$': wake,
    }
    for (timestamp, event) in events:
        for pattern in event_patterns:
            m = re.match(pattern, event)
            if m:
                event_patterns[pattern](m, timestamp, state)
                break
    return state['guards']


def process(puzzle_input):
    events = sorted(
        [parse_line(line) for line in puzzle_input], key=lambda x: x[0])
    guards = handle_events(events)

    # part one
    l = sorted(guards.items(), key=lambda x: sum(x[1]))
    max_minute = 0
    max_duration = 0
    for i, duration in enumerate(l[-1][1]):
        if duration > max_duration:
            max_duration = duration
            max_minute = i
    p1 = max_minute * l[-1][0]

    # part two
    p2_id = 0
    max_minute = 0
    max_duration = 0
    for guard in l:
        for i, duration in enumerate(guard[1]):
            if duration > max_duration:
                max_duration = duration
                max_minute = i
                p2_id = guard[0]
    p2 = p2_id * max_minute

    return (p1, p2)


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
