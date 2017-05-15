"""this function is to replace K and N in seq with one of A U G C"""
import copy


def replace(seq):
    rep_map = {"K": ["A", "C"], "N": ["A", "U", "G", "C"]}


    return total_seq


if __name__ == '__main__':
    seq = "GNKU"
    # output should be ["GAA", "GAC", "GUA", "GUC", "GGA", "GGC", "GCA", "GCC"]
    replaced = replace(seq)
    for r in replaced:
        print r
