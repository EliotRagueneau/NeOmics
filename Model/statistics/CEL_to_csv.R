library(affy)
setwd("~/Bureau/NeOmics/statistics/cel/")

# lecture des fichiers .CEL

files = list.files(full.names = TRUE)
affy.data = ReadAffy(filenames = files)

#normalisation

norm = rma(affy.data)
exp = exprs(norm)

summary(exp)


library("ath1121501.db")

x = ath1121501ACCNUM
mapped_probes = mappedkeys(x)
xx = as.list(x[mapped_probes])

# replacement sequence IDS with Locus IDS 
for(i in seq(1:nrow(exp))){
  if(!(xx[(rownames(exp)[i])] %in% rownames(exp))){
    rownames(exp)[i] = unique(xx[(rownames(exp)[i])])
  }
}

# swip
xxx = unlist(xx,use.names = F)
data_bis = subset(exp,(rownames(exp) %in% xxx))

write.csv(data_bis,"GSE7631_loc.csv")

# sauvegarde des donnees
write.csv(data_bis,"~/Bureau/NeOmics/data/GSE7631_loc.csv")
