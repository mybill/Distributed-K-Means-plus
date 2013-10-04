#!/usr/bin/python
import sys, random

if __name__ == '__main__':
	f = float(sys.argv[1])
	for line in sys.stdin:
		cols = line.strip().split('\t')
		p = float(cols[0])/f
		rand = random.random()
		if rand<p:
			print '\t'.join(cols[1:])
