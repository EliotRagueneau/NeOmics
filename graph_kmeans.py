# -*- coding: utf-8 -*-
# Edited on 5th june 2018

# packages

import sys, os, py2neo, csv
from py2neo import *

# Neo4j database connexion

ID = sys.argv[1]
password = sys.argv[2]
data = sys.argv[3]
title = sys.argv[4]

graph = Graph("bolt://localhost:11016", auth=("eliot", "1234"))


def create_tf_nodes(f):
    with open(f) as csvfile:
        tx = graph.begin()
        kmean = Node("Analysis", name=title)
        tx.create(kmean)
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)
        clusters = {}
        for row in reader:
            gene = graph.nodes.match("Gene", name=row[0]).first()
            cluster = row[1]
            if cluster not in clusters:
                cluster_node = Node("Cluster", id=cluster)
                clusters[cluster] = cluster_node
                tx.create(cluster_node)
                tx.merge(Relationship(cluster_node, "IS_CLUSTER_OF", kmean))
            if gene is not None:
                tx.create(Relationship(gene, "IS_IN_CLUSTER", clusters[cluster]))

    tx.commit()


def main():
    create_tf_nodes(data)


if __name__ == "__main__":
    main()
