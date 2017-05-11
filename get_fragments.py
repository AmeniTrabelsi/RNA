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


