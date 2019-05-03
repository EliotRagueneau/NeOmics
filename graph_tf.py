# -*- coding: utf-8 -*-
# Edited on 5th june 2018

# packages

import sys, os, py2neo, csv
from py2neo import *

# Neo4j database connexion

ID = sys.argv[1]
password = sys.argv[2]
data = sys.argv[3]

graph = Graph("bolt://localhost:11016", auth=("eliot", "1234"))


def create_tf_nodes(f):
    with open(f) as csvfile:
        tx = graph.begin()
        reader = csv.reader(csvfile, delimiter="\t")
        families = {}
        for row in reader:
            gene = graph.nodes.match("Gene", name=row[0]).first()
            fam = row[1]
            if fam not in families:
                z = Node("TF", family=fam)
                families[fam] = z
                tx.merge(z, primary_label="TF", primary_key="family")
            if gene is not None:
                tx.create(Relationship(gene, "IS_TF", families[fam]))

    tx.commit()


def main():
    create_tf_nodes(data)


if __name__ == "__main__":
    main()
