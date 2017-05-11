#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

iso_map = {'C': [12.0, 13.0033548378],
           'H': [1.00782503207, 2.0141017778],
           'O': [15.99491461956, 16.99913170, 17.9991610],
           'N': [14.0030740048, 15.0001088982],
           'S': [31.972071, 32.97145876, 33.96786690, 35.96708076],
           'P': [30.97376163]}

con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb");
with con:
    cur = con.cursor()
    cur.execute(" ")

