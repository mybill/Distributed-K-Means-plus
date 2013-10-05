#!/usr/bin/python
import sys, random, os, math

def upload_data(data_file, hdfs_dir):
	cmd = 'hadoop fs -mkdir %s' % (hdfs_dir)
	os.system(cmd)
	cmd = 'hadoop fs -put %s %s/datas' % (data_file, hdfs_dir)
	os.system(cmd)

def init_center(data_file):
	fin = open(data_file)
	lines = fin.readlines()
	fin.close()
	i = random.randint(0, len(lines)-1)
	fout = open('centers_seeds','w')
	fout.write(lines[i])
	fout.close()
	return len(lines[i].split('\t'))

def comp_dist(X,Y):
	if len(X)!=len(Y):
		return '-'
	sum = 0
	for i in xrange(len(X)):
		sum += math.pow(X[i]-Y[i], 2)
	return math.sqrt(sum)

def comp_diff(iter):
	diff = 0
	fc = open('centers_'+str(iter+1))
	for line in fc:
		cols = line.strip().split('\t')
		cid = int(cols[0])
		cc = map(float, cols[2:])
		diff += math.pow(comp_dist(centers[cid],cc), 2)
		centers[cid] = cc
	fc.close()
	return diff

def comp_f(iter):
	cmd = 'hadoop streaming \
		-input "%(hdfs_dir)s/datas" \
		-output "%(hdfs_dir)s/datas_r%(iter)d" \
		-mapper "python26/bin/python26.sh comp_dist.py" \
		-reducer NONE \
		-file comp_dist.py \
		-file centers_seeds \
		-cacheArchive "/share/python26.tar.gz#python26" \
		-jobconf mapred.map.tasks=20 \
		-jobconf mapred.job.name="mybill_kmeans++_compute"' % {
			'hdfs_dir':hdfs_dir,
			'iter':iter }
	cmd2 = 'hadoop streaming \
		-input "%(hdfs_dir)s/datas_r%(iter)d" \
		-output "%(hdfs_dir)s/datas_r%(iter)d_sum" \
		-mapper "python26/bin/python26.sh sum.py" \
		-reducer "python26/bin/python26.sh sum.py" \
		-file sum.py \
		-cacheArchive "/share/python26.tar.gz#python26" \
		-jobconf mapred.reduce.tasks=1 \
		-jobconf mapred.job.name="mybill_kmeans++_compute_sum"' % {
			'hdfs_dir':hdfs_dir,
			'iter':iter  }
	cmd3 = 'hadoop fs -cat %s/datas_r%d_sum/*' % (hdfs_dir, iter)
	os.system(cmd)
	os.system(cmd2)
	return float(os.popen(cmd3).read().strip())
		
def sample(iter, f):
	print 'sampling iteration %d ...' % (iter)
	cmd = 'hadoop streaming \
		-input "%(hdfs_dir)s/datas_r%(iter)d" \
		-output "%(hdfs_dir)s/centers_seeds_r%(iter)d" \
		-mapper "python26/bin/python26.sh sample.py %(f)d" \
		-reducer NONE \
		-file sample.py \
		-cacheArchive "/share/python26.tar.gz#python26" \
		-jobconf mapred.job.name="mybill_kmeans++_sample"' % {
			'hdfs_dir':hdfs_dir,
			'iter':iter,
			'f':f }
	cmd2 = 'hadoop fs -cat %s/centers_seeds_r%d/* >> centers_seeds' % (hdfs_dir, iter)
	os.system(cmd)
	os.system(cmd2)

def initialization(data_file, hdfs_dir, r, l):
	upload_data(data_file, hdfs_dir)
	size = init_center(data_file)

	sum = comp_f(0)
	print 'sum = %.2f' % (sum)
	if r==0:
		r = int(math.log(sum))
	print 'r = %d' % (r)
	
	for iter in xrange(r-1):
		sample(iter, sum/l)
		sum = comp_f(iter+1)	
	sample(r-1, sum/l)

	cmd = 'hadoop streaming \
		-input "%(hdfs_dir)s/datas" \
		-output "%(hdfs_dir)s/centers_seeds_weight" \
		-mapper "python26/bin/python26.sh seeds_weight.py mapper" \
		-reducer "python26/bin/python26.sh seeds_weight.py reducer" \
		-file seeds_weight.py \
		-file centers_seeds \
		-cacheArchive "/share/python26.tar.gz#python26" \
		-jobconf mapred.map.tasks=20 \
		-jobconf mapred.reduce.tasks=1 \
		-jobconf mapred.job.name="mybill_kmeans++_count_weight"' % {
		 	'hdfs_dir':hdfs_dir }
	cmd2 = 'rm centers_seeds_weight; hadoop fs -get %s/centers_seeds_weight/part-00000 centers_seeds_weight' % (hdfs_dir)
	os.system(cmd)
	os.system(cmd2)
	return size

def kmpp_sample(iter,filename):
	print 'kmeans++_sampling iteration %d' % (iter)
	fin = open(filename)
	lines = fin.readlines()
	fin.close()
	N = len(lines)
	p = [0]*N
	sum = 0
	for i in xrange(N):
		cols = lines[i].strip().split('\t',1)
		p[i] = float(cols[0])
		sum += p[i]
	rand = random.uniform(0,sum)
	for i in xrange(N):
		rand -= p[i]
		if rand<0:
			fout = open('centers_0','a')
			fout.write( '%d\t\t%s' % (iter, lines[i].split('\t',1)[1]) )
			fout.close()
			return

def read_center(filename):
	centers = []
	fc = open(filename)
	for line in fc:
		cols = line.strip().split('\t')
		centers.append(map(float,cols[2:]))
	fc.close()
	return centers

def comp_weight(data, centers, out):
	centers = read_center(centers)
	K = len(centers)
	dist = [0]*K
	fin = open(data)
	fout = open(out,'w')
	for line in fin:
		cols = line.strip().split('\t')
		instance = map(float,cols)
		for i in xrange(K):
			dist[i] = comp_dist(instance, centers[i])
		d = min(dist)
		fout.write( '%f\t%s' % (d*d, line) )
	fin.close()
	fout.close()
	
def kmpp(K):
	os.system('rm centers_0')
	kmpp_sample(0,'centers_seeds_weight')
	for i in xrange(1,K):
		comp_weight('centers_seeds','centers_0','centers_seeds_dist')
		kmpp_sample(i,'centers_seeds_dist')

if __name__ == '__main__':
	if len(sys.argv)!=6:
		print 'RUN: python run.py data_file K hdfs_dir r l/k'
	else:
		data_file = sys.argv[1]
		K = int(sys.argv[2])
		hdfs_dir = sys.argv[3]
		r = int(sys.argv[4])
		l = float(sys.argv[5])*K
		
		size = initialization(data_file, hdfs_dir, r, l)
		kmpp(K)

		centers = [[0 for col in range(size)] for row in range(K)]
		for iter in xrange(200):
			print 'Lloyd\' iteration %d ...' % (iter)
			cmd = "./iter.sh %d %s" % (iter, hdfs_dir)
			os.system(cmd)
			if comp_diff(iter)<1e-8:
				break
		print 'Clustering finish, result is in centers_%d' % (iter+1)
