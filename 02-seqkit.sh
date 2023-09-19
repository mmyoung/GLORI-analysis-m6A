#!/bin/bash
#
#$ -cwd
#$ -S /bin/bash
#$ -l p=6


## preprocess

printf "Deduplication ..."

## trim adapter and low quality bases

conda activate GLORI_env

for i in Sample1 Sample2 Sample3 Sample4
do
	mkdir -p /data/nym/20230625-AD-GLORI/analysis/seqkit/${i}
	cd /data/nym/20230625-AD-GLORI/analysis/seqkit/${i}

	filtered_fq=`ls /data/nym/20230625-AD-GLORI/analysis/trim_galore_res/${i}/*.fq`
	seqkit rmdup -j 4 -s -D ${i}_dup ${filtered_fq} >${i}_dedup.fq
done
