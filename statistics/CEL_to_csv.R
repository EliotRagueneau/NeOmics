library(affy)
setwd("./Bureau/gse7631/cel/")

# lecture des fichiers .CEL

files = list.files(full.names = TRUE)
affy.data = ReadAffy(filenames = files)

#normalisation

norm = rma(affy.data)
exp = exprs(norm)

summary(exp)

# sauvegarde des donnees
write.csv(exp,"GSE7631.csv")
