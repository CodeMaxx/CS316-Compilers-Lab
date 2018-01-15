import sys

inp = sys.stdin.readlines()

inp_list = []

#####################################
def split_num(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]
# Citation: https://stackoverflow.com/questions/5711452/how-do-i-slice-a-string-every-3-indices
#####################################

print(" " + inp[0])

for i in range(1, len(inp)):
    inp_list.append(split_num(inp[i].strip("\n"), 3))

rez = zip(*inp_list)

for i in rez:
    print(" ".join(i))
