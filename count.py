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
	sum = 0
	for i in xrange(len(X)):
		sum += math.pow(X[i]-Y[i], 2)
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
	centers = read_center('centers_seeds')
	K = len(centers)
	dist = [0]*K
	count = [0]*K
	for line in sys.stdin:
		instance = map(float, line.strip().split('\t'))
		for i in xrange(K):
			dist[i] = comp_dist(instance, centers[i])
		cid = argmin(dist)
		count[cid] += 1
	for cid in xrange(K):
		print '%d\t%d' % (cid, count[cid])

def reducer():
	fc = open('centers_seeds')
	centers = [line for line in fc]
	fc.close()
	
	K = len(centers)
	count = [0]*K
	for line in sys.stdin:
		cols = line.strip().split('\t')
		count[int(cols[0])] += int(cols[1])
	for i in xrange(K):
		print '%d\t%s' % (count[i], centers[i].strip())
		
#	cols = sys.stdin.readline().strip().split('\t')
#	last_cid = cols[0]
#	count = int(cols[1])
#	for line in sys.stdin:
#		cols = line.strip().split('\t')
#		cid = cols[0]
#		if cid==last_cid:
#			count += int(cols[1])
#		else:
#			print '%s\t%d' % (last_cid, count)
#			last_cid = cid
#			count = int(cols[1])
#	print '%s\t%d' % (last_cid, count)

if __name__ == '__main__':
	if sys.argv[1]=='mapper':
		mapper()
	elif sys.argv[1]=='reducer':
		reducer()
	else:
		print 'argument error!'
