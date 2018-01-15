import sys
from math import *

#####################################
def split_num(str, num):
    return [ str[start:start+num] for start in range(0, len(str), num) ]
# Citation: https://stackoverflow.com/questions/5711452/how-do-i-slice-a-string-every-3-indices
#####################################

def transpose_month(inp):
    inp_list = []

    for i in range(1, len(inp)):
        inp_list.append(split_num(inp[i].strip("\n"), 3))


    rez = zip(*inp_list)

    ret = ""

    k = []
    k.append(inp[0].strip("\n"))

    for i in rez:
        k.append(("".join(i)))

    return k

######################################################

inp = sys.stdin.readlines()

months = []

num = 1

print("          " + inp[0])

while(num+8 <= len(inp)):
    k = floor(num/9)
    months.append([])
    for f in range(3):
        months[k].append([])
    for i in inp[num:num+8]:
        j = i.strip("\n")
        l = 22
        for f in range(3):
            months[k][f].append(j[f*l : f*l + l])

    num += 9



for i in range(len(months)):
    for j in range(len(months[i])):
        for k in range(len(months[i][j])):
            months[i][j][k] += "\n"
        months[i][j] = transpose_month(months[i][j])

rez = list(zip(*months))


for i in rez:
    print("".join("%s" % k[0] for k in i))
    for j in range(1, len(i[0])):
        print(" ".join("%s" % k[j] for k in i))
