import MySQLdb as mdb

print "get data from Fragments Table"
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
# 'FragmentID', 'Name', 'Source', 'Fragment', 'MZ', 'RNAid', 'RawRNAid'
with con:
    cur = con.cursor()
    # query to get mz vs #sequence
    cur.execute("select nt.Fragment, nt.cnt from (select Fragment, count(distinct(RNAid)) as cnt from Fragments group by Fragment) as nt where nt.cnt > 1 order by nt.cnt desc")
    sequence_hist = cur.fetchall()
    # query to get mz vs #Fragment
    cur.execute("select nt.Fragment, nt.cnt from (select Fragment, count(*) as cnt from Fragments group by Fragment) as nt where nt.cnt > 1 order by nt.cnt desc")
    fragments_hist = cur.fetchall()

# you can plot or bar based on sequence_hist or fragments_hist

print "Done!"
