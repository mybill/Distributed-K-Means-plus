#!/bin/sh
HADOOP="/home/work/hadoop-client/hadoop/bin/hadoop"

${HADOOP} streaming \
	-input "${3}/datas_r${1}" \
	-output "${3}/centers_seeds_r${1}" \
	-mapper "python26/bin/python26.sh sample.py ${2}" \
	-reducer "cat" \
	-file sample.py \
	-cacheArchive "/share/python26.tar.gz#python26" \
	-jobconf mapred.map.tasks=20 \
	-jobconf mapred.reduce.tasks=1 \
	-jobconf mapred.job.name="mybill_kmeans++_sample"

exit 0
