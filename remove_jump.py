#!/usr/bin/env python

import sys, csv
from math import pi

def main():
    reader = csv.reader(sys.stdin)
    reader.next()
    data = [[float(x) for x in line] for line in reader]
    csv.writer(sys.stdout).writerows(remove_jump(data))
    
def remove_jump(data):
    column_len = len(data[0])
    flags =  [0] * column_len
    fixed = [data[0]]
    for i in range(1, len(data)):
        new = [0] * column_len
        for j in range(column_len):
            pre = data[i-1][j]
            cur = data[i][j]
            sign = cur * pre
            diff = abs(cur - pre)
            if(sign < 0 and (diff > pi * 1.5 and flags[j] == 0 or flags[j] != 0)): flags[j] += 1 if pre > 0 else -1
            if abs(flags[j]) > 1: raise Exception("error %(flags)s" % locals())
            new[j] = cur if(flags[j] == 0) else flags[j] * 2 * pi + cur
        fixed.append(new)

    return fixed

if __name__ == "__main__":
    main()
