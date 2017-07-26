#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql as mdb
import copy
import math

from mytools import find_set_with_index

iso_map = {'C': [12.0, 13.0033548378],
           'H': [1.00782503207, 2.0141017778],
           'O': [15.99491461956, 16.99913170, 17.9991610],
           'N': [14.0030740048, 15.0001088982],
           'S': [31.972071, 32.97145876, 33.96786690, 35.96708076],
           'P': [30.97376163],
           'Na': [22.9897692809],
           'K': [38.96370668, 39.96399848, 40.96182576]}
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
# Create a table called “Fragments”
# Compute the dictionary called “fragments” storing the related table information
#   Fields: FragmentID, Name, Source, Fragment, MZ, RNAID, RawRNAid
#   Get all data from table “RNA” into variable rawRNA
#   For each rna sequence, decompose into multiple fragments
#       Separate by “separate_by = ‘G’” as default
#       For each sub-sequence, compute MZ
# Write “fragments” into “Fragments” table in db

print("get data from RNA Table")
rawRNA = []  # fetch from RNA table, output values are ((RNAid, RawRNAid, Name, Source, Sequence))
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM RNA")
    raw_RNA_head = [i[0] for i in cur.description]
    rawRNA = cur.fetchall()

select_id = [176, 29509]
test_rawRNA = [rawRNA[i] for i in select_id]

print("RNA table head is {0}".format(raw_RNA_head))
print("For each rna sequence, decompose into multiple fragments")
head = ["Position_No", "RNA_ID", "Oligo_ID"]
all_fragments = []  # [[name1, source1, frag1, PositionStatus1, mz1, rnaid1, rawrnaid1], [name2, source2, frag2, PositionStatus2, mz2, rnaid2, rawrnaid2], ...]
separate_by = 'G'
total_num_data = len(test_rawRNA)
sort_value = []
for idx, line in enumerate(test_rawRNA):
    if idx % 1000 == 0:
        print("processing data at {0}%".format(100.0 * idx / total_num_data))
    rna_id = line[0]
    rna_sequence = line[-1]
    # compute fragments
    if idx == 0:
        all_fragments.append(['CGCACCA', '3prime', 1, rna_id])
        sort_value.append("".join(['CGCACCA', '_', '3prime']))
    else:
        all_fragments.append(['GUGUCGAU', '3prime', 1, rna_id])
        sort_value.append("".join(['GUGUCGAU', '_', '3prime']))


# calculate the unique fragment, all information of each unique fragment will be saved in one table
print("Total length of data to write into table AllFragments is {0}".format(len(all_fragments)))
print("Calculate the unique fragments")
head1 = ["Oligonucleotide", "Oligo_Type", "MW", "NO_A", "NO_U", "NO_G", "NO_C"]
# # get unique_fragment using np.unique
# u1, indices1 = np.unique(sort_value, return_index=True)
# u2, indices2 = np.unique(sort_value, return_inverse=True)
# unique_fragment = []
# for i, j in enumerate(indices1):
#     temp_info = all_fragments[j]
#     temp_index = np.where(indices2 == i)
#     unique_fragment.append(temp_info[2:4] + temp_info[5:] + list(temp_index[0]))
# # get unique_fragment using dictionary unsorted
unique_fragment = []
d = find_set_with_index(sort_value)
count_no = 1
for v in d.values():
    temp_info = copy.copy(all_fragments[v[0]])
    temp_frag = temp_info[0]
    temp_position = temp_info[1]
    for x in v:
        del all_fragments[x][0:2]
        all_fragments[x].append(count_no)
    # index_str = ",".join([str(x) for x in v])
    count_no += 1
    no_a = temp_frag.count('A')
    no_u = temp_frag.count('U')
    no_g = temp_frag.count('G')
    no_c = temp_frag.count('C')
    total_no = len(temp_frag)
    common_mz = total_no * mz_constant + mz_A * no_a + mz_U * no_u + mz_G * no_g + mz_C * no_c - total_no * \
                                                                                                 iso_map['H'][0]
    temp_mz = common_mz - iso_map['P'][0] - 2 * iso_map['O'][0] + iso_map['H'][0]

    unique_fragment.append([temp_frag, temp_position, temp_mz, no_a, no_u, no_g, no_c])


# print "Save all_fragments to file"
# pickle.dump(all_fragments, open("all_fragments.p", "wb"))
print("Total length of data to write into table Two_Oligonucleotides is {0}".format(len(all_fragments)))
print("Store the data into db")
placeholders = ", ".join(["%s"] * len(head))
columns = ", ".join(head)
myQuery = "INSERT INTO Two_Oligonucleotides ( %s ) VALUES ( %s )" % (columns, placeholders)
#
print("Total length of data to write into table Uni_Two_Oligos is {0}".format(len(unique_fragment)))
print("Store the data into db")
placeholders1 = ", ".join(["%s"] * len(head1))
columns1 = ", ".join(head1)
myQuery1 = "INSERT INTO Uni_Two_Oligos ( %s ) VALUES ( %s )" % (columns1, placeholders1)
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Two_Oligonucleotides")
    cur.execute("CREATE TABLE Two_Oligonucleotides(AllOligo_ID INT PRIMARY KEY AUTO_INCREMENT, \
                     Position_No VARCHAR(255), \
                     RNA_ID INT, \
                     Oligo_ID INT)")
    cur.execute("DROP TABLE IF EXISTS Uni_Two_Oligos")
    cur.execute("CREATE TABLE Uni_Two_Oligos(Oligo_ID INT PRIMARY KEY AUTO_INCREMENT, \
                         Oligonucleotide VARCHAR(255), \
                         Oligo_Type VARCHAR(255), \
                         MW VARCHAR(255), \
                         NO_A VARCHAR(255), \
                         NO_U VARCHAR(255), \
                         NO_G VARCHAR(255), \
                         NO_C VARCHAR(255))")
    # #  store by batch
    # batch = 200000
    # batch_num = int(math.ceil(1.0 * len(all_fragments) / batch))
    # for i in range(batch_num):
    #     print("batch save to Table Two_Oligonucleotides {0} of {1}".format(i+1, batch_num))
    #     cur.executemany(myQuery, all_fragments[i * batch : (i + 1) * batch])
    #  store all once if size is small
    cur.executemany(myQuery, all_fragments)
    # batch = 10000
    # batch_num = int(math.ceil(1.0 * len(unique_fragment) / batch))
    # for i in range(batch_num):
    #     print("batch save to Table Uni_Two_Oligos {0} of {1}".format(i+1, batch_num))
    #     cur.executemany(myQuery1, unique_fragment[i * batch : (i + 1) * batch])
    cur.executemany(myQuery1, unique_fragment)