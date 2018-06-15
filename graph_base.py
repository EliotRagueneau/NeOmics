#-*- coding: utf-8 -*-
# Edited on 5th june 2018

# packages

import sys,os,py2neo,csv
from py2neo import *



# Neo4j database connexion

ID = sys.argv[1]
password = sys.argv[2]
data = sys.argv[3]

py2neo.authenticate("localhost:7474",ID,password)

root_path = './Arabidopsis'
	
graph = Graph()

test_types = {"RP" : "deg", "wilcox" : "deg" , "wad" : "deg", "kmeans" : "clust", "hclust" : "clust"} 

def create_directory_nodes(p):
	
	for tissu in os.listdir(p):
		
		tx = graph.begin()
		# Si c'est un dossier
		if os.path.isdir(os.path.join(p,tissu)):
			
			x = Node("Tissu",name = tissu)
			tx.merge(x)
			
			for exp in os.listdir(os.path.join(p,tissu)):
				
				y = Node("Experience",name = exp,tissu = tissu)
				tx.merge(y)
				tx.merge(Relationship(x,"RELATED_TO",y))
				
				for analyse in os.listdir(os.path.join(p,tissu,exp)):
					
					with open (os.path.join(p,tissu,exp,analyse)) as csvfile:
						
						test_name = analyse[:-4]
						reader = csv.reader(csvfile, delimiter=" ")
						
						if test_types[test_name] == "deg":
							
							a = Node("Test", name = test_name, analysis_type = 'deg')
							b = Node("Group", name="up", test = test_name)
							c = Node("Group", name="down", test = test_name)
							tx.create(a)
							tx.create(b)
							tx.create(c)
							tx.merge(Relationship(a,"PERFORMED_ON",y))
							tx.merge(Relationship(b,"GROUP_OF",a))
							tx.merge(Relationship(c,"GROUP_OF",a))
							
							for row in reader:
								if row[0] != "NA":
									g_up = graph.find_one("Gene", "Entrez_id", row[0])
									tx.merge(Relationship(g_up,"IS_DEG",b))
								if row[1] != "NA":
									g_down = graph.find_one("Gene", "Entrez_id", row[1])
									tx.merge(Relationship(g_down,"IS_DEG",c))
							
				
		tx.commit()


def create_gene_nodes(f):
	with open(f) as csvfile:
		reader = csv.reader(csvfile, delimiter=",")
		for row in reader:
			graph.merge(Node("Gene", Entrez_id=row[0]))


def main():
	#create_gene_nodes(data)
	create_directory_nodes(root_path)
	


if __name__ == "__main__":
	main()
