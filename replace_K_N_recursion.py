"""this function is to replace K and N in seq with one of A U G C"""


rep_map = {"K": ["A", "C"], "N": ["A", "U", "G", "C"]}


def replace(output, tmp_output, seq):
    if len(seq) == 0:
        return output.append(tmp_output)
    else:
        if seq[0] not in rep_map.keys():
            replace(output, tmp_output + seq[0], seq[1:])
        else:
            for x in rep_map[seq[0]]:
                replace(output, tmp_output + x, seq[1:])
    return output


if __name__ == '__main__':
    seq = "GNK"
    # output should be ["GAA", "GAC", "GUA", "GUC", "GGA", "GGC", "GCA", "GCC"]
    replaced = replace([], '', seq)
    for r in replaced:
        print r
