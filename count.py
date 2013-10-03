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

def argmin(X):
	cid = 0
	min = X[0]
	for i,x in enumerate(X):
		if x<min:
			cid = i
			min = x
	return cid


def mapper():
	centers = read_center('centers_0_seeds')
	K = len(centers)
	dist = [0]*K
	count = [0]*K
	for line in sys.stdin:
		cols = line.strip().split('\t')
		for i in xrange(K):
			dist[i] = comp_dist(cols, centers[i])
		cid = argmin(dist)
		count[cid] += 1

	for cid in xrange(K):
		print '%d\t%d' % (cid, count[cid])


def reducer():
	last_cid = ''
	count = 0
	for line in sys.stdin:
		cols = line.strip().split('\t')
		cid = cols[0]
		if cid==last_cid:
			count += int(cols[1])
		else:
			if last_cid!='':
				print '%s\t%d' % (last_cid, count)
			last_cid = cid
			count = int(cols[1])
	print '%s\t%d' % (last_cid, count)

if __name__ == '__main__':
	if sys.argv[1]=='mapper':
		mapper()
	elif sys.argv[1]=='reducer':
		reducer()
	else:
		print 'argument error!'
