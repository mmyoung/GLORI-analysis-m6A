#!/bin/bash
#
#$ -cwd
#$ -S /bin/bash
#$ -l p=6



conda activate GLORI_env

Thread=4
genomdir=/data/nym/20230625-AD-GLORI/ref
genome=${genomdir}/mm10.AG_conversion.fa
genome2=/data/nym/reference/reference_mouse_mm10/Sequence/WholeGenomeFasta/mm10.fa
rvsgenome=${genomdir}/mm10.rvsCom.fa
TfGenome=${genomdir}/GCF_000001635.26_GRCm38_rna2.fa.AG_conversion.fa
annodir=/data/nym/20230625-AD-GLORI/ref
baseanno=${annodir}/GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl2.noredundance.base
anno=${annodir}/GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl2
outputdir=/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample1
tooldir=/data/nym/20230625-AD-GLORI/src/GLORI-tools-main

prx=Sample1
file=/data/nym/20230625-AD-GLORI/analysis/fastx_trimmer/Sample1/Sample1_trimmed.fq

mkdir -p $outputdir

python ${tooldir}/run_GLORI_back.py -i $tooldir -q ${file} -T $Thread -f ${genome} -f2 ${genome2} -rvs ${rvsgenome} -Tf ${TfGenome} -a $anno -b $baseanno -pre ${prx} -o $outputdir --combine --rvs_fac -c 1 -C 1 -r 0 -p 1.1 -adp 1.1 -s 0


outputdir=/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample2
prx=Sample2
file=/data/nym/20230625-AD-GLORI/analysis/fastx_trimmer/Sample2/Sample2_trimmed.fq
mkdir -p $outputdir

python ${tooldir}/run_GLORI_back.py -i $tooldir -q ${file} -T $Thread -f ${genome} -f2 ${genome2} -rvs ${rvsgenome} -Tf ${TfGenome} -a $anno -b $baseanno -pre ${prx} -o $outputdir --combine --rvs_fac -c 1 -C 1 -r 0 -p 1.1 -adp 1.1 -s 0


outputdir=/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample3
prx=Sample3
file=/data/nym/20230625-AD-GLORI/analysis/fastx_trimmer/Sample3/Sample3_trimmed.fq
mkdir -p $outputdir

python ${tooldir}/run_GLORI_back.py -i $tooldir -q ${file} -T $Thread -f ${genome} -f2 ${genome2} -rvs ${rvsgenome} -Tf ${TfGenome} -a $anno -b $baseanno -pre ${prx} -o $outputdir --combine --rvs_fac -c 1 -C 1 -r 0 -p 1.1 -adp 1.1 -s 0


outputdir=/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample4
prx=Sample4
file=/data/nym/20230625-AD-GLORI/analysis/fastx_trimmer/Sample4/Sample4_trimmed.fq
mkdir -p $outputdir

python ${tooldir}/run_GLORI.py -i $tooldir -q ${file} -T $Thread -f ${genome} -f2 ${genome2} -rvs ${rvsgenome} -Tf ${TfGenome} -a $anno -b $baseanno -pre ${prx} -o $outputdir --combine --rvs_fac -c 1 -C 1 -r 0 -p 1.1 -adp 1.1 -s 0
