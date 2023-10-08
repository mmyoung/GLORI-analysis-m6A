# GLORI-analysis-m6A
Customized analysis pipeline for GLORI-seq of m6A in mouse

Firstly, creating conda environment including following python modules:
`pysam,pandas,argparse,time,collections,os,sys,re,subprocess,multiprocessing,copy,numpy,scipy,math,sqlite3,Bio,statsmodels,itertools,heapq,glob,signal`

1. Download required references
```
download files for annotation
wget https://ftp.ncbi.nlm.nih.gov/refseq/M_musculus/annotation_releases/108.20200622/GCF_000001635.26_GRCm38.p6/GCF_000001635.26_GRCm38.p6_assembly_report.txt
wget https://ftp.ncbi.nlm.nih.gov/refseq/M_musculus/annotation_releases/108.20200622/GCF_000001635.26_GRCm38.p6/GCF_000001635.26_GRCm38.p6_genomic.gtf.gz

download reference genome and transcriptome
wget http://hgdownload.cse.ucsc.edu/goldenpath/mm10/bigZips/mm10.fa.gz
wget https://ftp.ncbi.nlm.nih.gov/refseq/M_musculus/annotation_releases/108.20200622/GCF_000001635.26_GRCm38.p6/GCF_000001635.26_GRCm38.p6_rna.fna.gz

```
2. Preprocessing of raw data with:

1) Trim adapter and low quality bases with trim_galore
2) Remove PCR duplication with seqkit
3) Remove UMI with fastx_trimmer

```
qsub 01-preprocess.sh
```

3. Preparing references

```
qsub ref_prepare.sh
```
