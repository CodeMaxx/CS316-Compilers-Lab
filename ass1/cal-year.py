import sys
from math import *

inp = sys.stdin.readlines()

months = []

num = 1

print("             " + inp[0])

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

rez = zip(*months)

for i in rez:
    for j in range(len(i[0])):
        print("".join("%s" % k[j] for k in i))
