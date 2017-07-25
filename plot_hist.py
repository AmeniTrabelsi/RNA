import pymysql as mdb
import matplotlib.pyplot as plt

print("get data from Two_oligo_FragmentIons Table")
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
# 'FragmentID', 'Name', 'Source', 'Fragment', 'MZ', 'RNAid', 'RawRNAid'
with con:
    cur = con.cursor()
    # query to get mz vs #Fragment
    cur.execute("select FragmentIonClass from Two_oligo_FragmentIons where Oligo_ID = 1")
    FragmentIonClass = cur.fetchall()
    cur.execute("SELECT MZ FROM Two_oligo_FragmentIons where Oligo_ID = 1")
    MZ = cur.fetchall()
    cur.execute("SELECT AdductIon FROM Two_oligo_FragmentIons where Oligo_ID = 1")
    AdductIon = cur.fetchall()

temp_fragment = []
temp_MZ = []
temp_AdductIon = []
for idx1, aaa in enumerate(FragmentIonClass):
    temp_fragment.append(aaa[0])
for idx2, bbb in enumerate(MZ):
    temp_MZ.append(bbb[0])
for idx3, ccc in enumerate(AdductIon):
    temp_AdductIon.append(ccc[0])
from mytools import find_set_with_index
# print "get data from Fragments Table"
# con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
# # 'FragmentID', 'Name', 'Source', 'Fragment', 'MZ', 'RNAid', 'RawRNAid'
# with con:
#     cur = con.cursor()
#     # query to get mz vs #sequence
#     cur.execute("select nt.Fragment, nt.cnt from (select Fragment, count(distinct(RNAid)) as cnt from Fragments group by Fragment) as nt where nt.cnt > 1 order by nt.cnt desc")
#     sequence_hist = cur.fetchall()
#     # query to get mz vs #Fragment
#     cur.execute("select nt.Fragment, nt.cnt from (select Fragment, count(*) as cnt from Fragments group by Fragment) as nt where nt.cnt > 1 order by nt.cnt desc")
#     fragments_hist = cur.fetchall()
# print("get data from Uni_Fragments Table")
# con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
# # 'FragmentID', 'Name', 'Source', 'Fragment', 'MZ', 'RNAid', 'RawRNAid'
# with con:
#     cur = con.cursor()
#     # query to get mz vs #Fragment
#     cur.execute("select MZ from Uni_Fragments")
#     mz_hist = cur.fetchall()
#     cur.execute("SELECT Fragment FROM Uni_Fragments")
#     temp_Fragment = cur.fetchall()
#
# mz_hist = [float(x[0]) for x in mz_hist]
# plt.figure()
# plt.hist(mz_hist, bins=30)
# plt.ylabel('Number of Fragment')
# plt.xlabel('Molecule weight')
# plt.rc('axes', labelsize=40)
# plt.rc('xtick', labelsize=10)
# plt.rc('ytick', labelsize=10)
# plt.savefig('flg1.png')
# plt.show()
#
# # you can plot or bar based on sequence_hist or fragments_hist
#
# temp_Fragment = [str(x[0]) for x in temp_Fragment]
# fragment_hist = []
# for a in temp_Fragment:
#     fragment_hist.append(len(a))
#
# plt.figure()
# plt.hist(fragment_hist, bins=30)
# plt.ylabel('Number of Fragment')
# plt.xlabel('Number of Base')
# plt.rc('axes', labelsize=20)
# plt.rc('xtick', labelsize=10)
# plt.rc('ytick', labelsize=10)
# plt.savefig('flg2.png')
# plt.show()
# # plt.close()
#
# print("Done!")