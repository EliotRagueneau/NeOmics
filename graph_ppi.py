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


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def create_ppi_nodes(f):
    with open(f) as csvfile:
        tx = graph.begin()
        reader = csv.reader(csvfile, delimiter="\t")
        counter = 0

        lines = file_len(f)
        for row in reader:
            counter += 1
            print("{:.2%}".format(counter / lines))
            g_a = graph.nodes.match("Gene", name=row[0]).first()
            g_b = graph.nodes.match("Gene", name=row[1]).first()
            if g_a is not None and g_b is not None:
                tx.create(Relationship(g_a, "INTERACT_WITH", g_b))

    tx.commit()


def main():
    create_ppi_nodes(data)


if __name__ == "__main__":
    main()
