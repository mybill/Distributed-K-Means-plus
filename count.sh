#!/bin/sh
HADOOP="/home/work/hadoop-client/hadoop/bin/hadoop"

${HADOOP} streaming \
	-input "${1}/datas" \
	-output "${1}/centers_seeds_weight" \
	-mapper "python26/bin/python26.sh count.py mapper" \
	-reducer "python26/bin/python26.sh count.py reducer" \
	-file count.py \
	-file centers_seeds \
	-cacheArchive "/share/python26.tar.gz#python26" \
	-jobconf mapred.map.tasks=20 \
	-jobconf mapred.reduce.tasks=1 \
	-jobconf mapred.job.name="mybill_kmeans++_count_weight"

exit 0
