#!/bin/bash
#
#$ -cwd
#$ -S /bin/bash
#$ -l p=6


## preprocess

printf "Fastx trimmer ..."

## trim adapter and low quality bases

conda activate GLORI_env

for i in Sample1 Sample2 Sample3 Sample4
do
	mkdir -p /data/nym/20230625-AD-GLORI/analysis/fastx_trimmer/${i}
	cd /data/nym/20230625-AD-GLORI/analysis/fastx_trimmer/${i}

	filtered_fq=/data/nym/20230625-AD-GLORI/analysis/seqkit/${i}/${i}_dedup.fq
	fastx_trimmer -Q 33 -f 11 -i $filtered_fq -o ${i}_trimmed.fq
done
