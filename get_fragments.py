#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import numpy as np

iso_map = {'C': [12.0, 13.0033548378],
           'H': [1.00782503207, 2.0141017778],
           'O': [15.99491461956, 16.99913170, 17.9991610],
           'N': [14.0030740048, 15.0001088982],
           'S': [31.972071, 32.97145876, 33.96786690, 35.96708076],
           'P': [30.97376163],
           'Na': [22.9897692809],
           'K': [38.96370668, 39.96399848, 40.96182576]}
RNA_A = {'C': 5, 'H': 5, 'N': 5}
RNA_U = {'C': 4, 'H': 4, 'N': 2, 'O': 2}
RNA_G = {'C': 5, 'H': 5, 'N': 5, 'O': 1}
RNA_C = {'C': 4, 'H': 5, 'N': 3, 'O': 1}
RNA_constant = {'C': 5, 'H': 7, 'O': 6, 'P': 1}
mz_A = 0
for key, value in RNA_A.items():
    mz_A = mz_A+value*iso_map[key][0]
mz_U = 0
for key, value in RNA_U.items():
    mz_U = mz_U+value*iso_map[key][0]
mz_G = 0
for key, value in RNA_G.items():
    mz_G = mz_G+value*iso_map[key][0]
mz_C = 0
for key, value in RNA_C.items():
    mz_C = mz_C+value*iso_map[key][0]
mz_constant = 0
for key, value in RNA_constant.items():
    mz_constant = mz_constant+value*iso_map[key][0]
# Algorithm
# Create a table called “Fragments”
# Compute the dictionary called “fragments” storing the related table information
#   Fields: FragmentID, Name, Source, Fragment, MZ, RNAID
#   Get all data from table “RawRNA” into variable rawRNA
#   For each rna sequence, decompose into multiple fragments
#       Separate by “separate_by = ‘G’” as default
#       For each sub-sequence, compute MZ
# Write “fragments” into “Fragments” table in db

# get data from RawRNA Table
rawRNA = []  # fetch from RawRNA table, output values are ((RNAID, Name, Source, Sequence))
head = []
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM RawRNA")
    head = [i[0] for i in cur.description]
    rawRNA = cur.fetchall()

# For each rna sequence, decompose into multiple fragments
all_fragments = {"Name": [], "Source": [], "Fragment": [], "MZ": [], "RNAID": []}
separate_by = 'G'
for line in rawRNA:
    rna_id = line[0]
    rna_name = line[1]
    rna_source = line[2]
    rna_sequence = line[-1]
    separate_idx = []
    fragments = []
    for i, c in enumerate(rna_sequence):
        if separate_by == c:
            separate_idx.append(i)
    for i, j in enumerate(separate_idx):
        if i == 0:
            fragments.append(rna_sequence[:j+1])
        else:
            fragments.append(rna_sequence[separate_idx[i-1]+1:separate_idx[i]+1])
    if len(rna_sequence) >= separate_idx[-1]+1:
        fragments.append(rna_sequence[separate_idx[-1]+1:])
    fragments_mz = []
    for i, temp_frag in enumerate(fragments):
        no_a = temp_frag.count('A')
        no_u = temp_frag.count('U')
        no_g = temp_frag.count('G')
        no_c = temp_frag.count('C')
        if i == 0:
            temp_mz = (no_a+no_u+no_g+no_c)*mz_constant+mz_A*no_a+mz_U*no_u+mz_G*no_g+mz_C*no_c-(no_a+no_u+no_g+no_c)*iso_map['H'][0]+iso_map['P'][0]+3*iso_map['O'][0]
        elif i == len(fragments)-1:
            temp_mz = (no_a+no_u+no_g+no_c)*mz_constant+mz_A*no_a+mz_U*no_u+mz_G*no_g+mz_C*no_c-(no_a+no_u+no_g+no_c)*iso_map['H'][0]-iso_map['P'][0]-3*iso_map['O'][0]
        else:
            temp_mz = (no_a+no_u+no_g+no_c)*mz_constant+mz_A*no_a+mz_U*no_u+mz_G*no_g+mz_C*no_c-(no_a+no_u+no_g+no_c)*iso_map['H'][0]
        fragments_mz.append(temp_mz)
    
# Store the dictionary data into db
valuesTranspose = np.ndarray.tolist(np.array(all_fragments.values()).T)
placeholders = ", ".join(["%s"] * len(all_fragments))
columns = ", ".join(all_fragments.keys())
myQuery = "INSERT INTO Fragments ( %s ) VALUES ( %s )" % (columns, placeholders)

con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Fragments")
    cur.execute("CREATE TABLE Fragments(FragmentID INT PRIMARY KEY AUTO_INCREMENT, \
                     Name VARCHAR(255), \
                     Source VARCHAR(255), \
                     Fragment VARCHAR(255), \
                     MZ VARCHAR(255), \
                     RNAID INT)")
    cur.executemany(myQuery, valuesTranspose)


