#!/usr/bin/python
import sys

if __name__ == '__main__':
	sum = 0
	for line in sys.stdin:
		sum += float(line.strip().split('\t',1)[0])
	print sum
