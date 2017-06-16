#!/usr/bin/python
# -*- coding: utf-8 -*-


def read_fa_to_dict(fname = "input_data/all-trnas.fa"):
    print("read data from file")
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

    # define the head variable
    rna_head = ["Name", "Source", "Ori_Seq"]
    rna_data = []  # [[name1, source1, seq1], [name2, source2, seq2], ...]
    print("get DNA info from array read from file")
    for line in array:
        line_split = line.split(" ")
        #if 'N' in line_split[-1] or 'K' in line_split[-1]:
        name = line_split[0].split("-")[-1]
        source = line_split[0].split(".")[0][1:]
        sequence = line_split[-1]
        rna_data.append([name, source, sequence])

    print("map from DNA to RNA")
    dna_rna_map = {"A": "U", "T": "A", "C": "G", "G": "C", "K": "K", "N": "N"}
    for idx, dna_data in enumerate(rna_data):
        dna_seq = dna_data[-1]
        rna_seq = []
        for dna in dna_seq:
            rna_seq.append(dna_rna_map[dna])
        rna_data[idx][-1] = "".join(rna_seq)

    print("Finish get rna data from file")
    return rna_head, rna_data
