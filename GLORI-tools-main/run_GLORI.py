"""Cong Liu Yi_lab, Peking University"""
import pandas as pd

"""Feb, 2021"""
"""Email: liucong-1112@pku.edu.cn"""
"""Usage: This program is used to run GLORI-tools"""
"""Input: [.fastq]"""

import os, sys
import argparse
import time
import subprocess
import os
import multiprocessing
from time import strftime
import re


def run_command(file,combine,untreated,rvs_fac,Threads):
    file3 = outputprefix + "_tf_rs.bam"
    file3_2 = outputprefix + "_rvs_rs.bam"
    file4 = outputprefix + ".trans2Genome.bam"
    file5 = outputprefix + "_rs.bam"
    file6 = outputprefix + ".trans2Genome.sorted.bam"
    file6_2 = outputprefix + "_merged_t.bam"
    file7_1 = outputprefix + "_merged.bam"
    file7_2 = outputprefix + "_merged.sorted.bam"
    file8 = outputprefix + ".pileup"
    chr_file = outputprefix + "_chrlist"
    global file9
    file9 = outputdir+"/"+prx+".referbase.mpi"
    mapping_1 = "python "+NStoolsdir+"mapping_reads.py -q "+ file +" -p "+ Threads + " -f "+ genome+ ' --FilterN '+FilterN
    mapping_2 = " -mulMax " + mulMax + " -t " + tool + " -m " + mismatch +" -pre "+ prx+ " -o " + outputdir
    if untreated:
        file3 = outputprefix + "_un_s.bam"
        file5 = outputprefix + "_s.bam"
        if combine:
            mapping_command = mapping_1 + " -Tf " + transgenome + mapping_2 + " --untreated --combine "
        else:
            mapping_command = mapping_1 + mapping_2 + " --untreated "
        finalbam = file7_2
        if combine:
            print("**************combine,untreated")
            print(mapping_command)
            subprocess.call(mapping_command, shell=True)
            print("python " + NStoolsdir + "Transcrip2genome.py --input " + file3 + " --output " + file4 + " --anno " + anno + " --fasta " + genome + " --sort --index")
            subprocess.call("python " + NStoolsdir + "Transcrip2genome.py --input " + file3 + " --output " + file4 +\
                            " --anno " + anno + " --fasta " + genome + " --untreated --sort --index",
                shell=True)
            subprocess.call("python " + NStoolsdir + "concat_bam.py -i " + file5 + " " + file6 + " -o " + file7_1 + " -t " + Threads + " --sort --index ",
                shell=True)
            sys.exit(0)
        else:
            print("**************uncombine,untreated")
            print(mapping_command)
            subprocess.call(mapping_command, shell=True)
            print("samtools view -F 4 -@ " + Threads + " -bS -h " + file5 + " | samtools sort -@ " + Threads + " > " + finalbam)
            subprocess.call("samtools view -F 4 -@ " + Threads + " -bS -h " + file5 + " | samtools sort -@ " + Threads + " > " + finalbam,
                shell=True)
            subprocess.call("samtools index " + finalbam, shell=True)
            sys.exit(0)

    else:
        if combine and rvs_fac:
            print("**************combine,treated")
            mapping_command = mapping_1 + " -rvs " + rvsref +" -Tf "+ transgenome + mapping_2 + " --combine "+ " --rvs_fac"
            subprocess.call(mapping_command, shell=True)
            print("python "+NStoolsdir+"Transcrip2genome.py --input " + file3 + " --output "+file4 + " --anno "+anno+" --fasta "+genome+" --sort --index")

            subprocess.call("python "+NStoolsdir+"Transcrip2genome.py --input " + file3 + " --output "+file4 + " --anno "+anno+" --fasta "+genome+" --sort --index",shell=True)
            subprocess.call("python "+NStoolsdir+"concat_bam.py -i " + file3_2 + " " + file5 + " -o " + file6_2 + " -t " + Threads + " --sort --index ",shell=True)
            filexx = file6_2[:-4]+'.sorted.bam'
            subprocess.call("python "+NStoolsdir+"concat_bam.py -i " + filexx + " " + file6 + " -o " + file7_1 + " -t " + Threads + " --sort --index ",shell=True)
            #subprocess.call("rm -f " + filexx+"*", shell=True)
            #subprocess.call("rm -f " + outputprefix +"*_un_2.fq", shell=True)
            #subprocess.call("rm -f " + outputprefix +"*.SJ.out.tab", shell=True)
            #subprocess.call("rm -f " + file3_2+"*", shell=True)
            #subprocess.call("rm -f " + file3+"*", shell=True)
            #subprocess.call("rm -f " + file5+"*", shell=True)
            print("rm -f " + file6+"*")
            #subprocess.call("rm -f " + file6+"*", shell=True)
            #subprocess.call("rm -f " + file7_1+"*", shell=True)
            #subprocess.call("rm -f " + file6_2+"*", shell=True)
            #subprocess.call("rm -f " + outputprefix + "_tf_rs.unlift.bam"+"*", shell=True)
            finalbam = file7_2
        elif not combine and not rvs_fac:
            print("**************uncombine,treated,no rvs_fac")
            mapping_command = mapping_1 + mapping_2
            print(mapping_command)
            subprocess.call(mapping_command, shell=True)
            finalbam = file7_2
            print("samtools view -F 20 -@ " + Threads + " -bS -h " + file5 + " | samtools sort -@ " + Threads + " > " + finalbam)
            subprocess.call("samtools view -F 20 -@ " + Threads + " -bS -h " + file5 + " | samtools sort -@ " + Threads + " > " + finalbam,shell=True)
            subprocess.call("samtools index " + finalbam, shell=True)

    subprocess.call("mkdir -p "+outputdir+"/mapping-info", shell=True)
    subprocess.call("mv "+outputprefix+"*out "+outputdir+"/mapping-info", shell=True)
    subprocess.call("mv "+outputprefix+"*put "+outputdir+"/mapping-info", shell=True)
    print("**********merged bam finished**************")
    print("python "+NStoolsdir+"pileup_genome_multiprocessing.py -P " + Threads + " -f " + genome + " -i " + finalbam + " -o " + file8)
    subprocess.call("python "+NStoolsdir+"pileup_genome_multiprocessing.py -P "+Threads+" -f "+genome+" -i "+ finalbam +" -o "+file8,shell=True)
    print("python "+NStoolsdir+"get_referbase.py -input " + file8 + " -referFa "+ genome2 + " -outname_prx "\
                    + outputdir +'/'+prx)
    subprocess.call("python "+NStoolsdir+"get_referbase.py -input " + file8 + " -referFa "+ genome2 + " -outname_prx "\
                    + outputdir +'/'+prx, shell=True)
    #subprocess.call("rm -f " + file8, shell=True)
    print("*************call sites****************")
    print("cut -f 1 "+file9 + " | sort -u > " + chr_file)
    subprocess.call("cut -f 1 "+file9 + " | sort -u > " + chr_file, shell=True)
    chr_list = sorted([r1.strip().split("\t")[0] for r1 in open(chr_file).readlines()])
    #
    fac_chr = True
    index = 0
    while fac_chr:
        chr_prx = chr_list[0][:3]
        detected_chr = [i.split('.')[-1]+"_AG_converted" for i in os.listdir(outputdir) if re.search(prx + ".referbase.mpi.formatted.txt." + chr_prx,i) and not re.search('tmp',i)]
        print("*************Detected",detected_chr,len(detected_chr))
        if len(detected_chr) == len(chr_list):
            print(index)
            fac_chr = False
            break
        print(index,'lalalalala')
        if index >= 12:
            print("Erro!!! break multiprocessing")
            fac_chr = False
        else:
            index += 1
            differ_chr = [i for i in chr_list if i not in detected_chr]
            print("**************No_Detected",differ_chr)
            multiprocessing.freeze_support()
            pool = multiprocessing.Pool(int(Threads))
            try:
                for chr in differ_chr:
                    pool.apply_async(func=get_sites, args=(chr,))
                pool.close()
                pool.join()
            finally:
                pool.terminate()

    print("**************optain totalsites******************")
    #subprocess.call("rm -f " + file9, shell=True)
    final_sites1 = outputprefix + ".totalm6A.txt"
    final_format = outputprefix + ".totalformat.txt"
    subprocess.call("cat " + outputprefix + ".referbase.mpi.formatted.txt" + ".* | sed '/#/d' > " + final_format,
                    shell=True)
    """Combing A-to-G conversion files"""
    print("**************Combing A-to-G conversion files******************")
    pd_CR = pd.DataFrame()
    final_CR = outputprefix + ".totalCR.txt"
    for CR_c in chr_list:
        chr_x = CR_c.split("_AG_converted")[0]
        file = outputprefix+".CR.txt."+chr_x
        CR1 = pd.read_csv(file, sep="\t", names=['SA', 'Totalcovered_reads', 'Remained A reads', 'Non-A-to-G ratio','Mapped_area'])
        CR2 = CR1[~CR1['SA'].isin(['#ALL', '#90%', '#75%', '#50%', '#25%', '#10%', '#Median', '#Mean'])][['SA', 'Non-A-to-G ratio']]
        xx_median = CR1[CR1['SA'] == '#Median']['Totalcovered_reads'].values.tolist()
        pd_median = pd.DataFrame({'SA': ["#Median_"+chr_x], 'Non-A-to-G ratio': xx_median})

        pd_CR_t = pd.concat([pd_median,CR2])
        pd_CR_t['A-to-G_ratio'] = 1 - pd_CR_t ['Non-A-to-G ratio']
        pd_x1 = pd_CR_t[['SA', 'A-to-G_ratio']]

        pd_CR = pd.concat([pd_CR, pd_x1])
    pd_CR.to_csv(final_CR,sep="\t",index=False)

    print("cat " + outputprefix + ".callsites" + "*." + str(Acutoffs) + ".txt > " + final_sites1)
    subprocess.call("cat " + outputprefix + ".callsites" + "*." + str(Acutoffs) + ".txt > " + final_sites1, shell=True)
    print("rm -f " + outputprefix + "*." + chr_prx + "* ")
    #subprocess.call("rm -f " + outputprefix + "*." + chr_prx + "* ", shell=True)
    #subprocess.call("rm -f " + chr_file, shell=True)
    """FDR filter"""
    final_sites2 = outputprefix + ".totalm6A.FDR"
    print("python " + NStoolsdir + "m6A_caller_FDRfilter.py -i " + final_sites1 + ' -o ' + final_sites2\
                    + ' -adp ' + adjP)
    subprocess.call("python " + NStoolsdir + "m6A_caller_FDRfilter.py -i " + final_sites1 + ' -o ' + final_sites2\
                    + ' -adp ' + adjP, shell=True)
    #subprocess.call("rm -f " + final_sites1, shell=True)


def get_sites(chr):
    print(chr)
    # time.sleep(1)
    chr2 = chr.split("_AG_converted")[0]
    baseanno_chr = baseanno + "." + chr2
    file_mpi = file9 + "." + chr2
    file_format = outputprefix + ".referbase.mpi.formatted.txt" + "." + chr2
    file_CR = outputprefix + ".CR.txt" + "." + chr2
    file_sites = outputprefix + ".callsites" + "." + chr2
    print("awk \'$1==\"\'\"" + chr + "\"\'\"\' " + file9 + " > " + file_mpi)
    subprocess.call("awk \'$1==\"\'\"" + chr + "\"\'\"\' " + file9 + " > " + file_mpi,shell = True)
    if baseanno != 'None':
        if not os.path.exists(baseanno_chr):
            print("awk \'$1==\"\'\"" + chr2 + "\"\'\"\' " + baseanno + " > " + baseanno_chr)
            subprocess.call("awk \'$1==\"\'\"" + chr2 + "\"\'\"\' " + baseanno + " > " + baseanno_chr,shell = True)
        print("python "+NStoolsdir+"m6A_pileup_formatter.py --db "+ baseanno_chr + " -i " + file_mpi + " -o "+ file_format +" --CR "+ file_CR)
        subprocess.call("python "+NStoolsdir+"m6A_pileup_formatter.py --db "+ baseanno_chr + " -i " + file_mpi + " -o "+file_format +" --CR "+ file_CR,shell=True)
    else:
        print("python " + NStoolsdir + "m6A_pileup_formatter.py " + " -i " + file_mpi + " -o " + file_format + " --CR " + file_CR)
        subprocess.call("python " + NStoolsdir + "m6A_pileup_formatter.py " + " -i " + file_mpi + " -o " + file_format + " --CR " + file_CR,
            shell=True)
    print("python "+NStoolsdir+"m6A_caller.py -i "+file_format + " -o " + file_sites +" -c " + Cov +" -C "+ Counts + " -r "\
                    + minRatio +" -p "+pvalue+" -s "+multiAratio+" -R "+AGRatio +" --cutoff " + Acutoffs +" --CR "+ \
                    background+" --method " + statmethod)
    subprocess.call("python "+NStoolsdir+"m6A_caller.py -i "+file_format + " -o " + file_sites +" -c " + Cov +" -C "+ Counts + " -r "\
                    + minRatio +" -p "+pvalue+" -s "+multiAratio+" -R "+AGRatio +" --cutoff " + Acutoffs +" --CR "+ \
                    background+" --method " + statmethod,shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GLORI-tools for detecting m6A sites from high-throughput sequencing data")

    group_required = parser.add_argument_group("Required")
    group_required.add_argument("-i", "--NSdir", nargs="?", type=str, default=sys.stdin,help = "Directory where GLORI-tool is located")
    group_required.add_argument("-q", "--fastq", nargs="?", type=str, default=sys.stdin,
                        help="fastq files with surfix as _1.fq;_1.fastq;_2.fq;_2.fastq")
    group_required.add_argument("-f", "--reference", nargs="?", type=str, default=sys.stdin, help="Index file for the plus strand of the genome")
    group_required.add_argument("-f2", "--reference2", nargs="?", type=str, default=sys.stdin, help="Index file for the unchanged genome")
    group_required.add_argument("-rvs", "--rvsref", nargs="?", type=str, default=sys.stdin, help = "Index file for the minus strand of the genome")
    group_required.add_argument("-Tf", "--transref", nargs="?", type=str, default='None',help="Index file for the minus strand of the transcriptome")
    group_required.add_argument("-a", "--anno", nargs="?", type=str, default='None', help="Annotation file within exons")
    group_required.add_argument("--combine", "--combine", help="Whether mapping to transcriptome",action="store_true")
    group_required.add_argument("--untreated", "--untreated", help="If the input is untreated",action="store_true")
    group_required.add_argument("--rvs_fac", "--rvs_fac",help="Whether to map to the reverse strand of the transcriptome", action="store_true")


    group_output = parser.add_argument_group("Output (optional)")
    group_output.add_argument("-pre", "--outname_prefix", nargs="?", type=str, default='default', help="Output file prefix")
    group_output.add_argument("-o", "--outputdir", nargs="?", type=str, default='./', help="Output directory")


    group_mappingfilter = parser.add_argument_group("Mapping conditions (optional)")

    group_mappingfilter.add_argument("-F", "--FilterN", nargs="?", type=str, default=0.5, help="The setting for the STAR parameter --outFilterScoreMinOverLread")
    group_mappingfilter.add_argument("-b", "--baseanno", nargs="?", type=str, default='None', help="Annotations at single-base resolution")
    group_mappingfilter.add_argument("-t", "--tools", nargs="?", type=str, default='STAR',  choices=['STAR', 'bowtie'],
                                     help="We recommend using STAR for genome alignment and Bowtie for transcriptome alignment.")
    group_mappingfilter.add_argument("-T", "--Threads", nargs="?", type=str, default='1',help="Used threads")
    group_mappingfilter.add_argument("-mulMax", "--mulMax", nargs="?", type=str, default='1',help="Suppress all alignments if > <int> exist")
    group_mappingfilter.add_argument("-m", "--mismatch", nargs="?", type=str, default='2', help="Permitted mapping mismatches")

    # Filter
    group_site = parser.add_argument_group("m6A filter (optional)")
    group_site.add_argument("-c", "--coverage", dest="coverage", default='15', type=str, help="A+G coverage")
    group_site.add_argument("-C", "--count", dest="count", default='5', type=str,help="A coverage")
    group_site.add_argument("-r", "--ratio", dest="ratio", default='0.1', type=str, help="m6A level or A rate")
    group_site.add_argument("-p", "--pvalue", dest="pvalue", default='0.005', type=str, help="P-value cutoff for statistical test")
    group_site.add_argument("-adp", "--adjustpvalue", dest="adjustpvalue", default='0.005', type=str, help="Cutoff for FDR-adjusted p-value")
    group_site.add_argument("-s", "--signal", dest="signal", default='0.8', type=str,
                            help="signal ratio, The reads coverage (below the A-cutoff) divided by the total coverage \
                            is used to exclude false positives located in regions resistant to nitrite treatment")
    group_site.add_argument("-R", "--var_ratio", dest="var_ratio", default='0.8', type=str,
                            help="The A+G coverage divided by the total coverage is used to exclude mapping errors")
    group_site.add_argument("-g", "--gene_CR", dest="gene_CR", default='0.2', type=str,
                            help="Any m6A sites within a gene with an A-to-G conversion rate below the cutoff will be discarded")
    group_site.add_argument("-N", "--AG", dest="AG_number", default=0, type=int,
                            help="Any m6A sites within a gene with an A+G coverage below the cutoff will be discarded")


    # Statistics
    group_stat = parser.add_argument_group("Statistic method (optional)")
    group_stat.add_argument("--method", dest="method", default="binomial", choices=['binomial', 'poisson'],
                            help="Statistical method to test the significance of m6A.")
    group_stat.add_argument("--CR", dest="conversion_rate", default="gene", choices=['gene', 'overall'],
                            help="The control conversion rate used to establish statistical models")
    group_stat.add_argument("--NA", dest="non_anno", default="ELSE",
                            choices=['ELSE', 'Median', 'Mean', 'ALL', 'discard'],
                            help="Determining which CR to use for the sites that are not annotated to any genes")
    group_stat.add_argument("--cutoff", dest="A_cutoffs", default="3", choices=["1","2","3","4","5","6","7","8","9","10","15","20","None"],
                            help="A-cutoffs, The cutoff for the minimum number of remained A bases in each read")

    options = parser.parse_args()
    global genome,genome2,transgenome, outputdir,tool,Threads,mulMax,mismatch,anno,baseanno,prx,rvsref,outputprefix,FilterN
    global Cov,Counts,minRatio,pvalue,adjP,multiAratio,AGRatio,geneCR,AG_number_gene,statmethod,background,NAbackground,Acutoffs
    NStoolsdir = options.NSdir+"/pipelines/"
    genome = options.reference
    genome2 = options.reference2
    transgenome = options.transref
    rvsref = options.rvsref
    outputdir = options.outputdir
    tool = options.tools
    Threads = options.Threads
    mulMax = options.mulMax
    mismatch = options.mismatch
    anno = options.anno
    baseanno = options.baseanno
    prx = options.outname_prefix
    Cov = options.coverage
    Counts = options.count
    minRatio = options.ratio
    pvalue = options.pvalue
    adjP=options.adjustpvalue
    multiAratio = options.signal
    AGRatio = options.var_ratio
    geneCR = options.gene_CR
    AG_number_gene = options.AG_number
    statmethod = options.method
    background = options.conversion_rate
    NAbackground = options.non_anno
    Acutoffs = options.A_cutoffs
    FilterN = str(options.FilterN)
    outputprefix = outputdir + "/" + prx
    if options.untreated:
        genome = genome.split(".AG_conversion.fa")[0]
        transgenome = transgenome.split(".AG_conversion.fa")[0]

    if baseanno == 'None':
        background = 'overall'
    run_command(options.fastq,options.combine,options.untreated,options.rvs_fac,Threads)


