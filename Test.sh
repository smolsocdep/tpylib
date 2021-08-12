#!/bin/sh
python3 -m doctest utilities.py  -v > test.log
python3 -m doctest paginator.py  -v >> test.log
cat test.log

