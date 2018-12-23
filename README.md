# aoc2018
My Advent of Code 2018 solutions

Should work in Python 2.7 and 3.x, but only tested in 3.7.

General usage should follow:
```
$ python3 day1.py input.txt
```

You can also enter input via stdin, use EOF marker (Ctrl+D) when finished sending input.
When using stdin, your input format should match the AOC txt file input format.
```
$ python3 day1.py -
1
2
3
<Ctrl+D>
```

### Requirements

- \[day 9\] [blist](http://stutzbachenterprises.com/blist/)
- \[day 23] [z3](https://github.com/Z3Prover/z3) (pip package is `z3-solver`)

### Optional

- [tqdm](https://github.com/tqdm/tqdm) - if tqdm is available, certain slow solutions will provide a progress bar on the terminal.

To install everything:
```
$ pip install -r requirements.txt
```
