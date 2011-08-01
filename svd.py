#!/usr/bin/end python

import sys, csv, scipy
from os.path import basename
from scipy.linalg import svd

def main():
    lines = []
    all_data = []
    for filename in sys.argv[1:]:
        data = scipy.genfromtxt(filename, delimiter = ",", skip_header = 1)
        lines.append(len(data))
        all_data.extend(data)

    [U, S, V] = svd(all_data)

    line = 0
    for i in range(len(lines)):
        csv.writer(open("svd_" + basename(sys.argv[i + 1]), "w")).writerows(U[line:(line + lines[i]), :6])
        line += lines[i]

if __name__ == "__main__":
    main()
