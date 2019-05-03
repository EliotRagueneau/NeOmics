# -*- coding: utf-8 -*-
# Edited on 5th june 2018

# packages

import sys, os, py2neo, csv
from py2neo import *

# Neo4j database connexion

ID = sys.argv[1]
password = sys.argv[2]
data = sys.argv[3]

graph = Graph("bolt://localhost:7687", auth=(ID, password))


def add_goi_label(f):
    with open(f) as csvfile:
        tx = graph.begin()
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            gene = graph.nodes.match("Gene", name=row[0]).first()
            if gene is not None:
                gene.update_labels(["Gene", "GOI"])
                print(gene)
                tx.push(gene)

    tx.commit()


def main():
    add_goi_label(data)


if __name__ == "__main__":
    main()
