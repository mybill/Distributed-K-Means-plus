#!/usr/bin/python
import sys, math

def read_center(filename):
	centers = []
	fc = open(filename)
	for line in fc:
		cols = line.strip().split('\t')
		centers.append(cols[:])
	fc.close()
	return centers

def comp_dist(X,Y):
	sum = 0
	for i in xrange(len(X)):
		sum += math.pow((float(X[i])-float(Y[i])), 2)
	return math.sqrt(sum)

def mapper():
	filename = sys.argv[2]
	centers = read_center(filename)
	K = len(centers)
	dist = [0]*K
	sum = 0
	for line in sys.stdin:
		cols = line.strip().split('\t')
		for i in xrange(K):
			dist[i] = comp_dist(cols, centers[i])
		sum += min(dist)
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
	else:
		print 'argument error!'
