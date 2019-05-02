# -*- coding: utf-8 -*-
# Edited on 5th june 2018

# packages

import csv
import py2neo
import sys

from py2neo import *

# Neo4j database connexion

ID = sys.argv[1]
password = sys.argv[2]
data = sys.argv[3]

py2neo.authenticate("localhost:7474", ID, password)

graph = Graph()


def create_ppi_nodes(f):
    with open(f) as csvfile:
        tx = graph.begin()
        reader = csv.reader(csvfile, delimiter="\t")
        for row in reader:
            print
            row[0], row[1]
            g_a = graph.find_one("Gene", "Entrez_id", row[0])
            g_b = graph.find_one("Gene", "Entrez_id", row[1])
            if g_a != None and g_b != None:
                z = Node("PPI", p1=row[0], p2=row[1])
                tx.create(z)
                tx.create(Relationship(g_a, "INTERACT_WITH", z))
                tx.create(Relationship(g_b, "INTERACT_WITH", z))

    tx.commit()


def main():
    create_ppi_nodes(data)


if __name__ == "__main__":
    main()
