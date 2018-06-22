setwd("~/Bureau/NeOmics/data")

data = read.csv("GSE7631_loc.csv",header=T,row.names = 1)


lateral_root_cap = data[,1:6]
epidermic_cortex = data[,7:12]
pericycle_root = data[,13:18]
protoplast_root = data[,19:24]

filtre_wilcox = function(condition1,condition2,alpha,type){
  # recupere les genes dont l'expression moyenne inter-groupe est significativement différente avec un test de wilcoxon
  if(nrow(condition1) != nrow(condition2)){
    return("the two conditions does not contain the same number of rows")
  }
  result = data.frame()
  for(gene in seq(1:nrow(condition1))){
    w=wilcox.test(as.matrix(condition1[gene,]),as.matrix(condition2[gene,]),alternative = type, exact=F)
    
    if(w$p.value<alpha){
      result = rbind(result,cbind(condition1[gene,],condition2[gene,]))
    }
  }
  return(result)
}

# hippocampe

pericycle_root_wilcox_less = filtre_wilcox(pericycle_root[,1:3],pericycle_root[,4:6],0.025,"l") # UP
pericycle_root_wilcox_great = filtre_wilcox(pericycle_root[,1:3],pericycle_root[,4:6],0.025,"g") # DOWN




write.table(wilballess$ENtrezGeneID,"~/NEOMICS/bdd/Souris/Hippocampe/BAL_LPS_affy/wilcox_up",row.names = F,col.names = F)
write.table(wilbalgreat$ENtrezGeneID,"~/NEOMICS/bdd/Souris/Hippocampe/BAL_LPS_affy/wilcox_down",row.names = F,col.names = F)
write.table(wildefless$ENtrezGeneID,"~/NEOMICS/bdd/Souris/Hippocampe/DEF_LPS_affy/wilcox_up",row.names = F,col.names = F)
write.table(wildefgreat$ENtrezGeneID,"~/NEOMICS/bdd/Souris/Hippocampe/DEF_LPS_affy/wilcox_down",row.names = F,col.names = F)
