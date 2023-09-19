#!/bin/bash
#
#$ -cwd
#$ -S /bin/bash
#$ -l p=20


## This is the complete procedures for indexing the genome and transcriptome
## including the code from ref_prepare_bowtie.sh script


## preprocess the reference genome
conda activate GLORI_env

src_dir=/data/nym/20230625-AD-GLORI/src
ref_dir=/data/nym/20230625-AD-GLORI/ref
genome_fastafile=/data/nym/reference/reference_mouse_mm10/Sequence/WholeGenomeFasta/mm10.fa

cd $ref_dir

python $src_dir/GLORI-tools-main/get_anno/change_UCSCgtf.py -i $ref_dir/GCF_000001635.26_GRCm38.p6_genomic.gtf -j $ref_dir/GCF_000001635.26_GRCm38.p6_assembly_report.txt -o GCF_000001635.26_GRCm38_genomic.gtf_change2Ens


python $src_dir/GLORI-tools-main/pipelines/build_genome_index.py -f $genome_fastafile -p 15 -t STAR -pre mm10 -o $ref_dir


python $src_dir/GLORI-tools-main/get_anno/gtf2anno.py -i GCF_000001635.26_GRCm38_genomic.gtf_change2Ens -o GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl

awk '$3!~/_/&&$3!="na"' GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl | sed '/unknown_transcript/d'  > GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl2

python $src_dir/GLORI-tools-main/get_anno/anno_to_base.py -i GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl2 -o GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl2.baseanno


python $src_dir/GLORI-tools-main/get_anno/selected_longest_transcrpts_fa.py -anno GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl2 -fafile GCF_000001635.26_GRCm38.p6_rna.fna --outname_prx GCF_000001635.26_GRCm38_rna2.fa

python $src_dir/GLORI-tools-main/pipelines/build_transcriptome_index.py -f GCF_000001635.26_GRCm38_rna2.fa -pre GCF_000001635.26_GRCm38_rna2.fa -t "bowtie2"


python $src_dir/GLORI-tools-main/get_anno/gtf2genelist.py -i GCF_000001635.26_GRCm38_genomic.gtf_change2Ens -f GCF_000001635.26_GRCm38.p6_rna.fna -o GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.genelist > output2

awk '$6!~/_/&&$6!="na"' GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.genelist > GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.genelist2

python $src_dir/GLORI-tools-main/get_anno/anno_to_base_remove_redundance_v1.0.py -i GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl2.baseanno -o GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.tbl2.noredundance.base -g GCF_000001635.26_GRCm38_genomic.gtf_change2Ens.genelist2



