#!/bin/sh
HADOOP="/home/work/hadoop-client/hadoop/bin/hadoop"

${HADOOP} streaming \
	-input "${3}/datas" \
	-output "${3}/${2}" \
	-mapper "python26/bin/python26.sh comp_f.py mapper ${1}" \
	-reducer "python26/bin/python26.sh comp_f.py reducer" \
	-file comp_f.py \
	-file ${1} \
	-cacheArchive "/share/python26.tar.gz#python26" \
	-jobconf mapred.map.tasks=20 \
	-jobconf mapred.reduce.tasks=1 \
	-jobconf mapred.job.name="mybill_kmeans++_compute"

exit 0
