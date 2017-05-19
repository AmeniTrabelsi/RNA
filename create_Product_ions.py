#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import math
# import pickle

iso_map = {'C': [12.0, 13.0033548378],
           'H': [1.00782503207, 2.0141017778],
           'O': [15.99491461956, 16.99913170, 17.9991610],
           'N': [14.0030740048, 15.0001088982],
           'S': [31.972071, 32.97145876, 33.96786690, 35.96708076],
           'P': [30.97376163],
           'Na': [22.9897692809],
           'K': [38.96370668, 39.96399848, 40.96182576]}
adduct_ions = {'H+': 1.00727645207,
               '+': -0.00054858,
               'Na+': 22.9892207009,
               'NH4+': 18.03382555308,
               'K+': 38.9631581,
               '-H2O+H+': -17.00328823163,
               'C2H4N+': 42.03382555308,
               'C2H3NNa+': 64.01576980191,
               'Pt(NH3)0(2+)': 189.95883484,
               'Pt(NH3)1(2+)': 206.98538394101,
               'Pt(NH3)2(2+)': 224.01193304202,
               'H-': -1.00727645207,
               '-': 0.00054858,
               'Cl-': 34.96940126,
               '-H2O-H-': -19.01784113577,
               '-2H+Na-': 20.97466779676}  # 0 to 10 are positive mode, 11 to 15 are negative mode
RNA_A = {'C': 5, 'H': 5, 'N': 5}
RNA_U = {'C': 4, 'H': 4, 'N': 2, 'O': 2}
RNA_G = {'C': 5, 'H': 5, 'N': 5, 'O': 1}
RNA_C = {'C': 4, 'H': 5, 'N': 3, 'O': 1}
RNA_constant = {'C': 5, 'H': 8, 'O': 6, 'P': 1}
mz_A = 0
for key, value in RNA_A.items():
    mz_A += value * iso_map[key][0]
mz_U = 0
for key, value in RNA_U.items():
    mz_U += value * iso_map[key][0]
mz_G = 0
for key, value in RNA_G.items():
    mz_G += value * iso_map[key][0]
mz_C = 0
for key, value in RNA_C.items():
    mz_C += value * iso_map[key][0]
mz_constant = 0
for key, value in RNA_constant.items():
    mz_constant += value * iso_map[key][0]

# Algorithm
# Create a table called “Product_ions”
# Compute the dictionary called “product_ions” storing the related table information
#   Fields: ProductIonsID, Name, Source, ProductIons, MZ, FragmentID, RNAID, RawRNAid
#   Get all data from table “Fragments” into variable fragments
#   For each fragment, calculates the a1...an;b1...bn;c1...cn;d1...dn;w1...wn;x1...xn;y1...yn;z1...zn;a-B.
#       For each ion, compute MZs in positive mode and negative mode
# Write “product_ions” into “Product_ions” table in db

print "get data from Fragments Table"
fragments = []  # fetch from Fragments table, output values are ((FragmentID, Name, Source, Fragment, MZ, RNAid, RawRNAid))
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Fragments")
    fragments_head = [i[0] for i in cur.description]
    fragments = cur.fetchall()