#!/bin/bash
#
#$ -cwd
#$ -S /bin/bash
#$ -l p=6


## preprocess

printf "Preprocessing raw data..."

## trim adapter and low quality bases

conda activate GLORI_env

raw_fq_data=/data/nym/20230625-AD-GLORI/raw_data/s348g01056_T185-20230616-L-01-2023-06-201642/Sample_SQ23020125-20230615-pwq-1-20230615-pwq-1/SQ23020125-20230615-pwq-1-20230615-pwq-1_combined_R2.fastq.gz
out_dir=/data/nym/20230625-AD-GLORI/analysis/trim_galore_res/Sample1

#mkdir -p $out_dir 

#trim_galore -q 20 --stringency 1 -e 0.3 --length 35 --dont_gzip -o $out_dir $raw_fq_data


raw_fq_data=/data/nym/20230625-AD-GLORI/raw_data/s348g01056_T185-20230616-L-01-2023-06-231744/Sample_SQ23020126-20230615-pwq-2-20230615-pwq-2/SQ23020126-20230615-pwq-2-20230615-pwq-2_combined_R2.fastq.gz
out_dir=/data/nym/20230625-AD-GLORI/analysis/trim_galore_res/Sample2

mkdir -p $out_dir

trim_galore -q 20 --stringency 1 -e 0.3 --length 35 --dont_gzip -o $out_dir $raw_fq_data


raw_fq_data=/data/nym/20230625-AD-GLORI/raw_data/s348g01056_T185-20230616-L-01-2023-06-201642/Sample_SQ23020127-20230615-pwq-3-20230615-pwq-3/SQ23020127-20230615-pwq-3-20230615-pwq-3_combined_R2.fastq.gz

out_dir=/data/nym/20230625-AD-GLORI/analysis/trim_galore_res/Sample3
mkdir -p $out_dir

trim_galore -q 20 --stringency 1 -e 0.3 --length 35 --dont_gzip -o $out_dir $raw_fq_data



raw_fq_data=/data/nym/20230625-AD-GLORI/raw_data/s348g01056_T185-20230616-L-01-2023-06-201642/Sample_SQ23020128-20230615-pwq-4-20230615-pwq-4/SQ23020128-20230615-pwq-4-20230615-pwq-4_combined_R2.fastq.gz

out_dir=/data/nym/20230625-AD-GLORI/analysis/trim_galore_res/Sample4
mkdir -p $out_dir

trim_galore -q 20 --stringency 1 -e 0.3 --length 35 --dont_gzip -o $out_dir $raw_fq_data
