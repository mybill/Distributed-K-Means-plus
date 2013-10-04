#!/usr/bin/python
import sys


def mapper():
	sum = 0
	for line in sys.stdin:
		sum += float(line.strip().split('\t')[0])
	print sum

def reducer():
	sum = 0
	for line in sys.stdin:
		sum += float(line.strip())
	print sum

if __name__ == '__main__':
	if sys.argv[1]=='mapper':
		mapper()
	elif sys.argv[1]=='reducer':
		reducer()
