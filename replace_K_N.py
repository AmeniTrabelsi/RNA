"""this function is to replace K and N in seq with one of A U G C"""


def replace(seq):
    rep_map = {"K": ["A", "C"], "N": ["A", "U", "G", "C"]}
    total_seq = []
    for i, each_letter in enumerate(seq):
        if i == 0:
            if each_letter in rep_map.keys():
                total_seq = rep_map[each_letter]
            else:
                total_seq = each_letter
        else:
            temp1 = []
            if each_letter in rep_map.keys():
                for temp_seq in total_seq:
                    for temp_S in rep_map[each_letter]:
                        temp1.append(temp_seq + temp_S)
            else:
                for temp_seq in total_seq:
                    temp1.append(temp_seq + each_letter)
            total_seq = temp1
    return total_seq


if __name__ == '__main__':
    seq = "GNKU"
    # output should be ["GAA", "GAC", "GUA", "GUC", "GGA", "GGC", "GCA", "GCC"]
    replaced = replace(seq)
    for r in replaced:
        print(r)
