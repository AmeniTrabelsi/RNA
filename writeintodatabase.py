#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import numpy as np
import read_fa_to_dict as readFAfile

# # instead of manually create the db, we can use python dictionary structure to write multiple column data into db
# # Google "python dictionary examples" if not familair with it
## here we have `myDict` to store everything with {key, value}
## you need to figure out the way to generate myDict in your case
## So learn to get your dictionary data first
myDict = readFAfile.read_fa_to_dict()

valuesTranspose = np.ndarray.tolist(np.array(myDict.values()).T)

##  after get your myDict ready, now you can write it into db
placeholders = ", ".join(["%s"] * len(myDict))
columns = ", ".join(myDict.keys())
myQuery = "INSERT INTO RawRNA ( %s ) VALUES ( %s )" % (columns, placeholders)

con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb");
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS RawRNA")
    cur.execute("CREATE TABLE RawRNA(RNAID INT PRIMARY KEY AUTO_INCREMENT, \
                 idx VARCHAR(255), \
                 Name VARCHAR(255), \
                 Source VARCHAR(255), \
                 Sequence TEXT)")
    cur.executemany(myQuery, valuesTranspose)