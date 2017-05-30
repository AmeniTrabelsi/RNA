

# find_set_with_index
# input: inp [xx, xxx, xxxx, ...]
# output: dict(key1=[idx1], ...)
def find_set_with_index(inp):
    output = {}
    for idx, v in enumerate(inp):
        if v not in output:
            output[v] = []
        output[v].append(idx)
    return output

