# NeOmics

Copyright (C) 2018  Léauté Ludovic 
 
 *  This file is part of NeOmics project
 
 * This project is free: you can redistribute it and/or modify it
 under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 * This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 RCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 
 * GNU General Public License for more details.


## Requirements (following information is for Linux only):

download neo4j communtity edition 

- neo4j (v3.1.1): download neo4j at https://neo4j.com/download/community-edition/

open your terminal and run the following command:

- systemctl {start|stop|restart} neo4j

You might now have access to the local interface running on port 7474.
To see the interface, open a web browser at the adress http://localhost:7474
If it is your first connexion enter your knew neo4j's username and password (and remember it)

install the neo4j-python managing package py2neo :

- python get-pip.py (if pip not already installed)

- pip install py2neo


## Database filling

- python3 graph_base.py neo4j <password> data/GSE7631_loc.csv
- python3 graph_goi.py neo4j <password> data/P_GOI.txt
- python3 graph_tf.py neo4j <password> data/P_TF_LABEL.txt
- python3 graph_ppi.py neo4j <password> data/P_PPI.txt  *(Long process)*
- python3 graph_kmeans.py neo4j <password> data/kmeans_5 KMEANS5 *(OPTIONAL)*




