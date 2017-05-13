import MySQLdb as mdb
import replace_K_N

print "get data from RawRNA Table"
# fetch from RawRNA table, output values are ((RawRNAid, Name, Source, Sequence))
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM RawRNA")
    rawRNA_head = [i[0] for i in cur.description]
    rawRNA = cur.fetchall()
print "RawRNA table head is {0}".format(rawRNA_head)

print "replace all K with A / C"
print "replace all N with A / U / G / C"
head = ["RawRNAid", "Name", "Source", "Sequence"]

data = []
for raw_rna in rawRNA:
    rna_list = list(raw_rna)
    rna_seq = rna_list[-1]
    if "K" not in rna_seq and "N" not in rna_seq:
        data.append(rna_list)
    else:
        rna_reps = replace_K_N.replace(rna_seq)
        for r_seq in rna_reps:
            data.append(rna_list[:-1] + [r_seq])

print "write data to RNA table in RNAdb database"
placeholders = ", ".join(["%s"] * len(head))
columns = ", ".join(head)
myQuery = "INSERT INTO RNA ( %s ) VALUES ( %s )" % (columns, placeholders)

con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS RNA")
    cur.execute("CREATE TABLE RNA(RNAid INT PRIMARY KEY AUTO_INCREMENT, \
                 RawRNAid INT, \
                 Name VARCHAR(255), \
                 Source VARCHAR(255), \
                 Sequence TEXT)")
    cur.executemany(myQuery, data)
