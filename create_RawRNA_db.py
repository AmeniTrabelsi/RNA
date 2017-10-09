#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql as mdb
import read_fa_to_dict as readFAfile

# # instead of manually create the db, we can use python [[], []] structure to write multiple column data into db
## here we have `data` to store everything with [[values1], [values2]]
## you need to figure out the way to generate data in your case
head, data = readFAfile.read_fa_to_dict("input_data/Ecoli user database.txt")

##  after get your table data ready, now you can write it into db
placeholders = ", ".join(["%s"] * len(head))
columns = ", ".join(head)
myQuery = "INSERT INTO Ori_tRNA_Ecoli ( %s ) VALUES ( %s )" % (columns, placeholders)

con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Ori_tRNA_Ecoli")
    cur.execute("CREATE TABLE Ori_tRNA_Ecoli(OriRNA_ID INT PRIMARY KEY AUTO_INCREMENT, \
                 Name VARCHAR(255), \
                 Source VARCHAR(255), \
                 Ori_Seq TEXT)")
    cur.executemany(myQuery, data)
