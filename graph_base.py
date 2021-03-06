# -*- coding: utf-8 -*-
# Edited on 5th june 2018

# packages

import sys, os, py2neo, csv
from py2neo import *

# Neo4j database connexion

ID = sys.argv[1]
password = sys.argv[2]
data = sys.argv[3]

root_path = './Arabidopsis'

graph = Graph("bolt://localhost:7687", auth=(ID, password))

test_types = {"RP": "deg", "wilcox": "deg", "wad": "deg", "kmeans": "clust", "hclust": "clust"}


def create_directory_nodes(p):
    for tissue in os.listdir(p):

        tx = graph.begin()
        # Si c'est un dossier
        if os.path.isdir(os.path.join(p, tissue)):

            tissue_node = Node("Tissue", name=tissue)
            tx.merge(tissue_node, primary_label="Tissue", primary_key="name")

            for exp_name in os.listdir(os.path.join(p, tissue)):

                exp_node = Node("Experience", name=exp_name, tissu=tissue)
                tx.merge(exp_node, primary_label="Experience", primary_key="name")
                tx.merge(Relationship(exp_node, "PERFORMED_ON", tissue_node))

                for analyse in os.listdir(os.path.join(p, tissue, exp_name)):

                    with open(os.path.join(p, tissue, exp_name, analyse)) as csvfile:

                        test_name = analyse[:-4]
                        reader = csv.reader(csvfile, delimiter=" ")

                        if test_types[test_name] == "deg":

                            analysis_node = Node("Analysis", name=test_name, analysis_type='deg')
                            up_group = Node("Group", name="up", test=test_name)
                            down_group = Node("Group", name="down", test=test_name)
                            tx.create(analysis_node)
                            tx.create(up_group)
                            tx.create(down_group)
                            tx.merge(Relationship(analysis_node, "RELATED_TO", exp_node))
                            tx.merge(Relationship(analysis_node, "ABOUT", tissue_node))
                            tx.merge(Relationship(up_group, "GROUP_OF", analysis_node))
                            tx.merge(Relationship(down_group, "GROUP_OF", analysis_node))

                            for row in reader:
                                if row[0] != "NA":
                                    g_up = graph.nodes.match("Gene", name=row[0]).first()
                                    tx.merge(Relationship(g_up, "IS_DEG", up_group))
                                if row[1] != "NA":
                                    g_down = graph.nodes.match("Gene", name=row[1]).first()
                                    tx.merge(Relationship(g_down, "IS_DEG", down_group))

        tx.commit()


def create_gene_nodes(f):
    with open(f) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for row in reader:
            graph.create(Node("Gene", name=row[0]))


def main():
    create_gene_nodes(data)
    create_directory_nodes(root_path)


if __name__ == "__main__":
    main()
