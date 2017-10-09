#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql as mdb
import math
# import pickle

iso_map = {'C': [12.0, 13.0033548378],
           'H': [1.00782503207, 2.0141017778],
           'O': [15.99491461956, 16.99913170, 17.9991610],
           'N': [14.0030740048, 15.0001088982],
           'S': [31.972071, 32.97145876, 33.96786690, 35.96708076],
           'P': [30.97376163],
           'Na': [22.9897692809],
           'K': [38.96370668, 39.96399848, 40.96182576]}
adduct_ions = {'H+': [1.00727645207, 'Positive'],
               '+': [-0.00054858, 'Positive'],
               'Na+': [22.9892207009, 'Positive'],
               'NH4+': [18.03382555308, 'Positive'],
               'K+': [38.9631581, 'Positive'],
               '-H2O+H+': [-17.00328823163, 'Positive'],
               'C2H4N+': [42.03382555308, 'Positive'],
               'C2H3NNa+': [64.01576980191, 'Positive'],
               'Pt(NH3)0(2+)': [189.95883484, 'Positive'],
               'Pt(NH3)1(2+)': [206.98538394101, 'Positive'],
               'Pt(NH3)2(2+)': [224.01193304202, 'Positive'],
               'H-': [-1.00727645207, 'Negative'],
               '-': [0.00054858, 'Negative'],
               'Cl-': [34.96940126, 'Negative'],
               '-H2O-H-': [-19.01784113577, 'Negative'],
               '-2H+Na-': [20.97466779676, 'Negative']}  # 0 to 10 are positive mode, 11 to 15 are negative mode
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
# Create a table called “Product_ions”
# Compute the dictionary called “product_ions” storing the related table information
#   Fields: ProductIonsID, Name, Source, ProductIons, MZ, FragmentID, RNAID, RawRNAid
#   Get all data from table “Fragments” into variable fragments
#   For each fragment, calculates the a1...an;b1...bn;c1...cn;d1...dn;w1...wn;x1...xn;y1...yn;z1...zn;a-B.
#       For each ion, compute MZs in positive mode and negative mode
# Write “product_ions” into “Product_ions” table in db

print("get data from Fragments Table")
fragments = []  # fetch from Fragments table, output values are ((FragmentID, Name, Source, Fragment, MZ, RNAid, RawRNAid))
con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM tRNA_UniOligos_Ecoli_T1")
    fragments_head = [i[0] for i in cur.description]
    fragments = cur.fetchall()

# fragments = []
# fragments.append(temp_fragments[1])
# fragments.append(temp_fragments[0])
print("ProductIon table head is {0}".format(fragments_head))
print("For each fragment, calculate all product ion and corresponding mzs")
head = ["Oligo_ID", "Oligonucleotide", "Oligo_Type", "FragmentIon", "FragmentIonClass", "AdductIon", "AdductIonType", "MZ"]
all_production = []  # [[name1, source1, production1, productionclass1, adductsion1, adductsiontype1, mz1, fragmentid1, rnaid1, rawrnaid1], [name2, source2, production2, productionclass2, adductsion2, adductsiontype2, mz2, fragmentid2, rnaid2, rawrnaid2], ...]
productionclass = {'a': 1, 'b': 1, 'c': 1, 'd': 1, 'a-B': 1, 'w': 2, 'x': 2, 'y': 2, 'z': 2}
total_num_data = len(fragments)
for idx, line in enumerate(fragments):
    if idx % 1000 == 0:
        print("processing data at {0}%".format(100.0 * idx / total_num_data))
    oligo_id = line[0]
    oligo_seq = line[1][::-1]
    oligo_type = line[2]
    No_letter = line[3:]
    # compute ProductIon
    temp_ion = []
    no_letter = len(oligo_seq)
    for i, temp_letter in enumerate(oligo_seq):
        if i != no_letter-1:
            for j in productionclass:
                if productionclass[j] == 1:
                    temp_positionclass = j + str(i + 1)
                    temp1 = oligo_seq[:i+1]
                    no_a = temp1.count('A')
                    no_u = temp1.count('U')
                    no_g = temp1.count('G')
                    no_c = temp1.count('C')
                    total_no = len(temp1)
                    common_mz = total_no * mz_constant + mz_A * no_a + mz_U * no_u + mz_G * no_g + mz_C * no_c - total_no * iso_map['H'][0]
                    if j == 'a':
                        #########phosphate group
                        if oligo_type == '5Prime':
                            temp_mz = common_mz + iso_map['H'][0]
                        else:
                            temp_mz = common_mz - iso_map['P'][0] - 3 * iso_map['O'][0]
                        #########OH group
                        # if oligo_type == '5Prime':
                        #     temp_mz = common_mz + 2 * iso_map['H'][0]
                        # else:
                        #     temp_mz = common_mz - iso_map['P'][0] - 3 * iso_map['O'][0]
                    elif j == 'b':
                        #########phosphate group
                        if oligo_type == '5Prime':
                            temp_mz = common_mz + iso_map['H'][0] + iso_map['O'][0]
                        else:
                            temp_mz = common_mz - iso_map['P'][0] - 2 * iso_map['O'][0]
                        #########OH group
                        # if oligo_type == '5Prime':
                        #     temp_mz = common_mz + 2 * iso_map['H'][0] + iso_map['O'][0]
                        # else:
                        #     temp_mz = common_mz - iso_map['P'][0] - 2 * iso_map['O'][0]
                    elif j == 'c':
                        #########phosphate group
                        if oligo_type == '5Prime':
                            temp_mz = common_mz + 2 * iso_map['H'][0] + 3 * iso_map['O'][0] + iso_map['P'][0]
                        else:
                            temp_mz = common_mz + iso_map['H'][0]
                        #########OH group
                        # if oligo_type == '5Prime':
                        #     temp_mz = common_mz + 3 * iso_map['H'][0] + 3 * iso_map['O'][0] + iso_map['P'][0]
                        # else:
                        #     temp_mz = common_mz + iso_map['H'][0]
                    elif j == 'd':
                        #########phosphate group
                        if oligo_type == '5Prime':
                            temp_mz = common_mz + 2 * iso_map['H'][0] + 4 * iso_map['O'][0] + iso_map['P'][0]
                        else:
                            temp_mz = common_mz + iso_map['H'][0] + iso_map['O'][0]
                        #########OH group
                        # if oligo_type == '5Prime':
                        #     temp_mz = common_mz + 3 * iso_map['H'][0] + 4 * iso_map['O'][0] + iso_map['P'][0]
                        # else:
                        #     temp_mz = common_mz + iso_map['H'][0] + iso_map['O'][0]
                    elif j == 'a-B':
                        letterB = temp1[-1]
                        if letterB == 'A':
                            mz_B = mz_A
                        elif letterB == 'U':
                            mz_B = mz_U
                        elif letterB == 'G':
                            mz_B = mz_G
                        elif letterB == 'C':
                            mz_B = mz_C
                        #########phosphate group
                        if oligo_type == '5Prime':
                            temp_mz = common_mz + iso_map['H'][0] - mz_B
                        else:
                            temp_mz = common_mz - iso_map['P'][0] - 3 * iso_map['O'][0] - mz_B
                        #########OH group
                        # if oligo_type == '5Prime':
                        #     temp_mz = common_mz + 2 * iso_map['H'][0] - mz_B
                        # else:
                        #     temp_mz = common_mz - iso_map['P'][0] - 3 * iso_map['O'][0] - mz_B
                elif productionclass[j] == 2:
                    temp_positionclass = j + str(no_letter - i - 1)
                    temp1 = oligo_seq[i+1:]
                    no_a = temp1.count('A')
                    no_u = temp1.count('U')
                    no_g = temp1.count('G')
                    no_c = temp1.count('C')
                    total_no = len(temp1)
                    common_mz = total_no * mz_constant + mz_A * no_a + mz_U * no_u + mz_G * no_g + mz_C * no_c - total_no * iso_map['H'][0]
                    if j == 'w':
                        #########phosphate group
                        if oligo_type == '3Prime':
                            temp_mz = common_mz + iso_map['H'][0] + iso_map['O'][0]
                        else:
                            temp_mz = common_mz + 2 * iso_map['H'][0] + 4 * iso_map['O'][0] + iso_map['P'][0]
                        #########OH group
                        # if oligo_type == '3Prime':
                        #     temp_mz = common_mz + iso_map['H'][0] + iso_map['O'][0]
                        # else:
                        #     temp_mz = common_mz + 2 * iso_map['H'][0] + 3 * iso_map['O'][0] + iso_map['P'][0]
                    elif j == 'x':
                        #########phosphate group
                        if oligo_type == '3Prime':
                            temp_mz = common_mz + iso_map['H'][0]
                        else:
                            temp_mz = common_mz + 2 * iso_map['H'][0] + 3 * iso_map['O'][0] + iso_map['P'][0]
                        #########OH group
                        # if oligo_type == '3Prime':
                        #     temp_mz = common_mz + iso_map['H'][0]
                        # else:
                        #     temp_mz = common_mz + 2 * iso_map['H'][0] + 2 * iso_map['O'][0] + iso_map['P'][0]
                    elif j == 'y':
                        #########phosphate group
                        if oligo_type == '3Prime':
                            temp_mz = common_mz - iso_map['P'][0] - 2 * iso_map['O'][0]
                        else:
                            temp_mz = common_mz + iso_map['H'][0] + iso_map['O'][0]
                        #########OH group
                        # if oligo_type == '3Prime':
                        #     temp_mz = common_mz - iso_map['P'][0] - 2 * iso_map['O'][0]
                        # else:
                        #     temp_mz = common_mz + iso_map['H'][0]
                    elif j == 'z':
                        #########phosphate group
                        if oligo_type == '3Prime':
                            temp_mz = common_mz - iso_map['P'][0] - 3 * iso_map['O'][0]
                        else:
                            temp_mz = common_mz + iso_map['H'][0]
                        #########OH group
                        # if oligo_type == '3Prime':
                        #     temp_mz = common_mz - iso_map['P'][0] - 3 * iso_map['O'][0]
                        # else:
                        #     temp_mz = common_mz + iso_map['H'][0] - iso_map['O'][0]
                temp_ion = oligo_seq + '_' + temp_positionclass
                temp_adducts = {'H-', '-'}
                for temp1_adducts in temp_adducts:
                    temp_adduct_mz = temp_mz + 2*adduct_ions[temp1_adducts][0]
                    all_production.append([oligo_id, oligo_seq[::-1], oligo_type, temp_ion, temp_positionclass, temp1_adducts, adduct_ions[temp1_adducts][1], temp_adduct_mz])



print("Total length of data to write into mysql is {0}".format(len(all_production)))
print("Store the data into db")
placeholders = ", ".join(["%s"] * len(head))
columns = ", ".join(head)
myQuery = "INSERT INTO tRNA_Ecoli_T1_FragmentIons ( %s ) VALUES ( %s )" % (columns, placeholders)

con = mdb.connect("localhost", "xiaoli", "shumaker344", "RNAdb")
with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS tRNA_Ecoli_T1_FragmentIons")
    cur.execute("CREATE TABLE tRNA_Ecoli_T1_FragmentIons(FragmentIonID INT PRIMARY KEY AUTO_INCREMENT, \
                     Oligo_ID VARCHAR(255), \
                     Oligonucleotide VARCHAR(255), \
                     Oligo_Type VARCHAR(255), \
                     FragmentIon VARCHAR(255), \
                     FragmentIonClass VARCHAR(255), \
                     AdductIon VARCHAR(255), \
                     AdductIonType VARCHAR(255), \
                     MZ VARCHAR(255))")
    # # #  store by batch
    # batch = 200000
    # batch_num = int(math.ceil(1.0 * len(all_production) / batch))
    # for i in range(batch_num):
    #     print("batch save to mysql {0} of {1}".format(i+1, batch_num))
    #     cur.executemany(myQuery, all_production[i * batch : (i + 1) * batch])
    # #  store all once if size is small
    cur.executemany(myQuery, all_production)