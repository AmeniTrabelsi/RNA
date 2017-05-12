#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import read_fa_to_dict as readFAfile

# # instead of manually create the db, we can use python [[], []] structure to write multiple column data into db
## here we have `data` to store everything with [[values1], [values2]]
## you need to figure out the way to generate data in your case
head, data = readFAfile.read_fa_to_dict()

##  after get your table data ready, now you can write it into db
placeholders = ", ".join(["%s"] * len(head))
columns = ", ".join(head)
myQuery = "INSERT INTO RawRNA ( %s ) VALUES ( %s )" % (columns, placeholders)

con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS RawRNA")
    cur.execute("CREATE TABLE RawRNA(RNAID INT PRIMARY KEY AUTO_INCREMENT, \
                 Name VARCHAR(255), \
                 Source VARCHAR(255), \
                 Sequence TEXT)")
    cur.executemany(myQuery, data)
