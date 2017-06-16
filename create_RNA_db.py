import pymysql as mdb
import replace_K_N
import math

print("get data from OriRNA Table")
# fetch from RawRNA table, output values are ((RawRNAid, Name, Source, Sequence))
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM OriRNA")
    rawRNA_head = [i[0] for i in cur.description]
    rawRNA = cur.fetchall()
print("RawRNA table head is {0}".format(rawRNA_head))

print("replace all K with A / C")
print("replace all N with A / U / G / C")
head = ["OriRNA_ID", "Sequence"]

data = []
data_Large_KN = []
for raw_rna in rawRNA:
    rna_list = list(raw_rna)
    rna_seq = rna_list[-1]
    no_K = rna_seq.count('K')
    no_N = rna_seq.count('N')
    if no_K > 20 or no_N > 10:
        data_Large_KN.append([rna_list[0], rna_seq])
    elif no_K == 0 and no_N == 0: #"K" not in rna_seq and "N" not in rna_seq:
        data.append([rna_list[0], rna_seq])
    else: #(no_K <= 20 and no_K >= 1) or (no_N <= 10 and no_N >= 1):
        rna_reps = replace_K_N.replace(rna_seq)
        for r_seq in rna_reps:
            data.append([rna_list[0], r_seq])

print("write data to RNA table in RNAdb database")
placeholders = ", ".join(["%s"] * len(head))
columns = ", ".join(head)
myQuery1 = "INSERT INTO RNA ( %s ) VALUES ( %s )" % (columns, placeholders)
myQuery2 = "INSERT INTO RNA_large_KN ( %s ) VALUES ( %s )" % (columns, placeholders)

con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS RNA")
    cur.execute("CREATE TABLE RNA(RNA_ID INT PRIMARY KEY AUTO_INCREMENT, \
                 OriRNA_ID INT, \
                 Sequence TEXT)")
    cur.execute("DROP TABLE IF EXISTS RNA_large_KN")
    cur.execute("CREATE TABLE RNA_large_KN(RNA_ID INT PRIMARY KEY AUTO_INCREMENT, \
                 OriRNA_ID INT, \
                 Sequence TEXT)")
    # #  store by batch
    batch = 200000
    batch_num = int(math.ceil(1.0 * len(data) / batch))
    for i in range(batch_num):
        print("batch save to mysql {0} of {1}".format(i+1, batch_num))
        cur.executemany(myQuery1, data[i * batch : (i + 1) * batch])
    # #  store all once if size is small
    # cur.executemany(myQuery, data)
    cur.executemany(myQuery2, data_Large_KN)