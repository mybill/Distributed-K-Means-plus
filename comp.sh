#!/bin/sh
HADOOP="/home/work/hadoop-client/hadoop/bin/hadoop"

${HADOOP} streaming \
	-input "${2}/datas" \
	-output "${2}/datas_r${1}" \
	-mapper "python26/bin/python26.sh comp.py centers_seeds" \
	-reducer NONE \
	-file comp.py \
	-file centers_seeds \
	-cacheArchive "/share/python26.tar.gz#python26" \
	-jobconf mapred.map.tasks=20 \
	-jobconf mapred.job.name="mybill_kmeans++_compute"

exit 0
