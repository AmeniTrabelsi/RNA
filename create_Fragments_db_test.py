#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import math
import copy
import numpy as np
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

print "get data from RNA Table"
rawRNA = []  # fetch from RNA table, output values are ((RNAid, RawRNAid, Name, Source, Sequence))
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM RNA")
    raw_RNA_head = [i[0] for i in cur.description]
    rawRNA_all = cur.fetchall()
rawRNA = rawRNA_all[:100]
print "RNA table head is {0}".format(raw_RNA_head)
print "For each rna sequence, decompose into multiple fragments"
head = ["Position_No", "RNA_ID", "Frag_ID"]
all_fragments = []  # [[name1, source1, frag1, PositionStatus1, mz1, rnaid1, rawrnaid1], [name2, source2, frag2, PositionStatus2, mz2, rnaid2, rawrnaid2], ...]
separate_by = 'G'
total_num_data = len(rawRNA)
sort_value = []
for idx, line in enumerate(rawRNA):
    if idx % 1000 == 0:
        print "processing data at {0}%".format(100.0 * idx / total_num_data)
    rna_id = line[0]
    rna_sequence = line[-1]
    separate_idx = []
    # compute fragments
    fragments = []
    position_status = []
    position_no = []
    for i, c in enumerate(rna_sequence):
        if separate_by == c:
            separate_idx.append(i)
    count_no = 1
    for i, j in enumerate(separate_idx):
        if i == 0:
            fragments.append(rna_sequence[:j + 1])
            position_status.append('Start')
        else:
            fragments.append(rna_sequence[separate_idx[i - 1] + 1:separate_idx[i] + 1])
            position_status.append('Middle')
        position_no.append(count_no)
        count_no += 1
    if len(rna_sequence) >= separate_idx[-1] + 1:
        fragments.append(rna_sequence[separate_idx[-1] + 1:])
        position_status.append('End')
        position_no.append(count_no)
    else:
        position_status[-1] = 'End'
    # add fragment to all_fragments
    for i, temp_frag in enumerate(fragments):
        all_fragments.append([temp_frag, position_status[i], position_no[i], rna_id])
        sort_value.append("".join([temp_frag, '_', position_status[i]]))


head1 = ["Fragment", "Frag_Type", "MZ", "NO_A", "NO_U", "NO_G", "NO_C"]
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
    if i == 0:
        temp_mz = common_mz + iso_map['P'][0] + 3 * iso_map['O'][0] + 2 * iso_map['H'][0]
    elif i == total_no - 1:
        temp_mz = common_mz - iso_map['P'][0] - 3 * iso_map['O'][0] - iso_map['H'][0]
    else:
        temp_mz = common_mz + iso_map['H'][0]
    unique_fragment.append([temp_frag, temp_info[1], temp_mz, no_a, no_u, no_g, no_c])

# print "Save all_fragments to file"
# pickle.dump(all_fragments, open("all_fragments.p", "wb"))
print "Total length of data to write into mysql is {0}".format(len(all_fragments))
print "Store the data into db"
placeholders = ", ".join(["%s"] * len(head))
columns = ", ".join(head)
myQuery = "INSERT INTO Fragments_test ( %s ) VALUES ( %s )" % (columns, placeholders)


with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Fragments_test")
    cur.execute("CREATE TABLE Fragments_test(FragmentID INT PRIMARY KEY AUTO_INCREMENT, \
                     Name VARCHAR(255), \
                     Source VARCHAR(255), \
                     Fragment VARCHAR(255), \
                     Position VARCHAR(255), \
                     MZ VARCHAR(255), \
                     RNAid INT, \
                     RawRNAid INT)")
    # #  store by batch
    batch = 200000
    batch_num = int(math.ceil(1.0 * len(all_fragments) / batch))
    for i in range(batch_num):
        print "batch save to mysql {0} of {1}".format(i+1, batch_num)
        cur.executemany(myQuery, all_fragments[i * batch : (i + 1) * batch])
    # #  store all once if size is small
    # cur.executemany(myQuery, all_fragments)

