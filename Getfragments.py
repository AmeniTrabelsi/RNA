#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
dna_rna_map = {'C': [12.000000000], 'H': [], 'O': [], 'N': [], 'P': []}
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb");
with con:
    cur = con.cursor()
    cur.execute(" ")

