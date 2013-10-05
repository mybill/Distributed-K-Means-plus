#!/usr/bin/python
import sys, math

def read_center(filename):
	centers = []
	fc = open(filename)
	for line in fc:
		cols = line.strip().split('\t')
		centers.append(map(float,cols))
	fc.close()
	return centers

def comp_dist(X,Y):
	if len(X)!=len(Y):
		return '-'
	sum = 0
	for i in xrange(len(X)):
		sum += math.pow(X[i]-Y[i], 2)
	return math.sqrt(sum)


if __name__ == '__main__':
	centers = read_center('centers_seeds')
	K = len(centers)
	dist = [0]*K
	for line in sys.stdin:
		cols = line.strip().split('\t')
		instance = map(float,cols)
		for i in xrange(K):
			dist[i] = comp_dist(instance, centers[i])
		d = min(dist)
		print '%f\t%s' % (d*d, line.strip())
