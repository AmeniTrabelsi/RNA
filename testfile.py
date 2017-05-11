#!/usr/bin/python
# -*- coding: utf-8 -*-

fname = "input_data/all-trnas.fa"
print "read data from file"
array = []  # odd lines store info, even lines store sequence
flag = False  # flag is used to indicate this is the second+ line for sequence
with open(fname, "r") as lines:
    for line in lines:
        line = line.strip()
        if line.startswith('>'):
            array.append(line)
            flag = False
        else:
            if not flag:
                array[-1] += " " + line
                flag = True
            else:
                array[-1] += line

# define the dict variable
rna_data = {"idx": [], "Name": [], "Source": [], "Sequence": []}
print "get DNA info from array read from file"
count = 0
for line in array:
    line_split = line.split(" ")
    if 'N' not in line_split[-1] and 'K' not in line_split[-1]:
        rna_data["idx"].append(count)
        rna_data["Name"].append(line_split[0].split("-")[-1])
        rna_data["Source"].append(line_split[0].split(".")[0][1:])
        rna_data["Sequence"].append(line_split[-1])
        count += 1

print "map from DNA to RNA"
dna_rna_map = {"A": "U", "T": "A", "C": "G", "G": "C"}
for id, dna_seq in enumerate(rna_data["Sequence"]):
    rna_seq = []
    for dna in dna_seq:
        rna_seq.append(dna_rna_map[dna])
    rna_data["Sequence"][id] = "".join(rna_seq)


print "Finish get rna data from file"
