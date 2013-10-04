#!/bin/sh
HADOOP="/home/work/hadoop-client/hadoop/bin/hadoop"

${HADOOP} streaming \
	-input "${2}/datas_r${1}" \
	-output "${2}/datas_r${1}_sum" \
	-mapper "python26/bin/python26.sh sum.py mapper" \
	-reducer "python26/bin/python26.sh sum.py reducer" \
	-file sum.py \
	-cacheArchive "/share/python26.tar.gz#python26" \
	-jobconf mapred.map.tasks=20 \
	-jobconf mapred.reduce.tasks=1 \
	-jobconf mapred.job.name="mybill_kmeans++_compute_sum"

exit 0
