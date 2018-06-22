library("limma")

setwd("~/Bureau/NeOmics/")

data = read.csv("data/GSE7631.csv",header=T,row.names = 1)

lateral_root_cap = data[,1:6]
epidermic_cortex = data[,7:12]
pericycle_root = data[,13:18]
protoplast_root = data[,19:24]

grp.cl = c(0,0,0,1,1,1)

design = model.matrix(~grp.cl)
fit = lmFit(lateral_root_cap,design)
fit = eBayes(fit)
dim(fit)
genes = topTable(fit,number = 22810,p.value=0.999)
volcanoplot(fit,coef=2,highlight=nrow(genes))
limmaUp = genes[which(genes$logFC>0),]
limmaDown = genes[which(genes$logFC<0),]

write.table(limmaUp$ID,"limma_up",row.names = F,col.names = F)
write.table(limmaDown$ID,"limma_down",row.names = F,col.names = F)

limmaUp$ID
limmaDown$ID