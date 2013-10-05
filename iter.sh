#!/bin/sh
OUTPUT="${2}/centers_$((${1}+1))"

hadoop streaming \
	-input "${2}/datas" \
	-output ${OUTPUT} \
	-mapper "python26/bin/python26.sh mapper.py ${1}" \
	-reducer "python26/bin/python26.sh reducer.py" \
	-file mapper.py \
	-file reducer.py \
	-file centers_${1} \
	-cacheArchive "/share/python26.tar.gz#python26" \
	-jobconf mapred.map.tasks=20 \
	-jobconf mapred.job.map.capacity=20 \
	-jobconf mapred.reduce.tasks=2 \
	-jobconf mapred.job.reduce.capacity=2 \
	-jobconf mapred.job.name="mybill_kmeans-${1}"

hadoop fs -cat ${OUTPUT}/* > centers_$((${1}+1))

exit 0
