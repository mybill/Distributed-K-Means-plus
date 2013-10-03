#!/usr/bin/python
import sys, random, os, math

def upload_data(data_file, hdfs_dir):
	cmd = 'hadoop fs -mkdir %s' % (hdfs_dir)
	os.system(cmd)
	cmd = 'hadoop fs -put %s %s/datas' % (data_file, hdfs_dir)
	os.system(cmd)

def init_centers(data_file):
	fin = open(data_file)
	lines = fin.readlines()
	fin.close()

	centers = random.sample(range(len(lines)), 1)
	fout = open('centers_0_0','w')
	for t in centers:
		cols = lines[t].strip().split('\t')
		fout.write( '%f\t%f\n' % (float(cols[0]), float(cols[1])) )
	fout.close()

def comp_dist(X,Y):
	sum = 0
	for i in xrange(len(X)):
		sum += math.pow((float(X[i])-float(Y[i])), 2)
	return math.sqrt(sum)

def comp_diff(iter):
	diff = 0
	fc = open('centers_'+str(iter+1))
	for line in fc:
		cols = line.strip().split('\t')
		cid = int(cols[0])
		diff += comp_dist(centers[cid], cols[2:])
		centers[cid] = cols[2:]
	fc.close()
	return diff

if __name__ == '__main__':
	if len(sys.argv)!=5:
		print 'RUN: python run.py data_file size K hdfs_dir'
	else:
		data_file = sys.argv[1]
		size = int(sys.argv[2])
		K = int(sys.argv[3])
		hdfs_dir = sys.argv[4]
		L = int(sys.argv[5])
	
		upload_data(data_file, hdfs_dir)
		init_centers(data_file)

		cmd = './comp_f.sh centers_0_0 centers_0_f %s' % (hdfs_dir)
		cmd2 = 'hadoop fs -cat %s/centers_0_f/*' % (hdfs_dir)
		os.system(cmd)
		F = float(os.popen(cmd2).read().strip())
		print F
		tt = int(math.log10(F)+1)
		print tt
	
	
		for iter in xrange(tt):
			cmd = './comp_f.sh centers_0_seeds centers_0_f %s' % (hdfs_dir)
			cmd2 = 'hadoop fs -cat %s/centers_0_f/*' % (hdfs_dir)
			os.system(cmd)
			F = float(os.popen(cmd2).read().strip())
		
			cmd = './sample.sh %s %d' % (hdfs_dir, L)
			cmd2 = 'hadoop fs -cat %s/centers_0_%d/* >> centers_0_seeds' % (hdfs_dir, iter)
			os.system(cmd)
			os.system(cmd2)
			
		cmd = './count.sh %s' % (hdfs_dir)
		os.system(cmd)

		
		#centers = [[0 for col in range(size)] for row in range(K)]
		#for iter in xrange(200):
		#	cmd = "./iter.sh %d %d %d %s" % (iter,size,K,hdfs_dir)
		#	os.system(cmd)
		#	if comp_diff(iter)<1e-15:
		#		break
