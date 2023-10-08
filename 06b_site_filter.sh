cat diff_gr.txt | awk 'NR==1||$10<0.05' >diff_gr_p0.05.txt

awk 'BEGIN{OFS="\t"}NR==FNR {a[$1"_"$2]=$4}NR>FNR{print $0,a[$1"_"$2]}' ../GLORI_call_site/Sample1/Sample1.totalm6A.FDR.csv diff_gr_p0.05.txt >diff_gr_p0.05_gene.txt


cat diff_gr_filter_2.txt | awk 'NR==1||$10<0.05' >diff_gr_p0.05_filter_2.txt
awk 'BEGIN{OFS="\t"}NR==FNR {a[$1"_"$2]=$4}NR>FNR{print $0,a[$1"_"$2]}' ../GLORI_call_site/Sample1/Sample1.totalm6A.FDR.csv diff_gr_p0.05_filter_2.txt >diff_gr_p0.05_filter_2_gene.txt

