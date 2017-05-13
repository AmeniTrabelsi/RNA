"""this function is to replace K and N in seq with one of A U G C"""


def replace(seq):
    rep_map = {"K": ["A", "C"], "N": ["A", "U", "G", "C"]}

    return ["A", "C"] # something


if __name__ == '__main__':
    seq = "GNK"
    # output should be ["GAA", "GAC", "GUA", "GUC", "GGA", "GGC", "GCA", "GCC"]
    replaced = replace(seq)
    for r in replaced:
        print r
