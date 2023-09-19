## conda activate methylSig
library(methylSig)
library(bsseq)
library(data.table)

setwd("/data/nym/20230625-AD-GLORI/analysis/methylSig")
for (i in c(1,2,3,4)){
	tmp_df <- read.table(paste0("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample",i,"_filtered_m6A_2.txt"),header=T,stringsAsFactors=F)
	assign(paste0("S",i),tmp_df)
}

#S1 <- read.table("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample1/Sample1.totalm6A.FDR.csv",header=T,stringsAsFactors=F)
#S1 <- read.table("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample1_filtered_m6A.txt",header=T,stringsAsFactors=F)
row.names(S1) <- apply(S1,1,function(x) paste(x[c(1,2)],collapse="_"))
#S2 <- read.table("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample2/Sample2.totalm6A.FDR.csv",header=T,stringsAsFactors=F)
#S2 <- read.table("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample2_filtered_m6A.txt",header=T,stringsAsFactors=F)
row.names(S2) <- apply(S2,1,function(x) paste(x[c(1,2)],collapse="_"))
#S3 <- read.table("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample3/Sample3.totalm6A.FDR.csv",header=T,stringsAsFactors=F)
#S3 <- read.table("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample3_filtered_m6A.txt",header=T,stringsAsFactors=F)
row.names(S3) <- apply(S3,1,function(x) paste(x[c(1,2)],collapse="_"))
#S4 <- read.table("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample4/Sample4.totalm6A.FDR.csv",header=T,stringsAsFactors=F)
#S4 <- read.table("/data/nym/20230625-AD-GLORI/analysis/GLORI_call_site/Sample4_filtered_m6A.txt",header=T,stringsAsFactors=F)
row.names(S4) <- apply(S4,1,function(x) paste(x[c(1,2)],collapse="_"))


common_peak <- intersect(intersect(intersect(row.names(S1), row.names(S2)),row.names(S3)),row.names(S4))

M_mat <- cbind(S1[common_peak,"Acov",drop=FALSE],S2[common_peak,"Acov",drop=FALSE],S3[common_peak,"Acov",drop=FALSE],S4[common_peak,"Acov",drop=FALSE])
#colnames(M_mat) <- c("S1","S2","S3","S4")

cov_mat <- cbind(S1[common_peak,"AGcov",drop=FALSE],S2[common_peak,"AGcov",drop=FALSE],S3[common_peak,"AGcov",drop=FALSE],S4[common_peak,"AGcov",drop=FALSE])
#colnames(cov_mat) <- c("S1","S2","S3","S4")
rownames(M_mat) <- NULL
colnames(M_mat) <- NULL
rownames(cov_mat) <- NULL
colnames(cov_mat) <- NULL


BStmp <- BSseq(chr = S2[common_peak,"Chr"], pos=S2[common_peak,"Sites"], 
               M = as.matrix(M_mat), Cov = as.matrix(cov_mat), sampleNames = c("S1","S2","S3","S4"))

collapseBSseq(BStmp, group = c("WT", "WT", "AD","AD"))
pData(BStmp) <- data.frame(group = c("WT", "WT", "AD","AD"),row.names=sampleNames(BStmp))

diff_gr = diff_methylsig(
	bs = BStmp,
	group_column = 'group',
	comparison_groups = c('case' = 'AD', 'control' = 'WT'),
	disp_groups = c('case' = TRUE, 'control' = TRUE),
	local_window_size = 0,
	t_approx = TRUE,
	n_cores = 1)

diff_bino = diff_binomial(
	bs = BStmp,
        group_column = 'group',
	comparison_groups = c('case' = 'AD', 'control' = 'WT'))
#write.table(as.data.frame(diff_bino),file="/data/nym/20230625-AD-GLORI/analysis/methylSig/diff_binomial.txt",sep="\t",quote=F,row.names=F)

#write.table(as.data.frame(diff_gr),file="/data/nym/20230625-AD-GLORI/analysis/methylSig/diff_gr.txt",sep="\t",quote=F,row.names=F)
write.table(as.data.frame(diff_bino),file="/data/nym/20230625-AD-GLORI/analysis/methylSig/diff_binomial_filter_2.txt",sep="\t",quote=F,row.names=F)
write.table(as.data.frame(diff_gr),file="/data/nym/20230625-AD-GLORI/analysis/methylSig/diff_gr_filter_2.txt",sep="\t",quote=F,row.names=F)


