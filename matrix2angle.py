#!/usr/bin/env python

import sys, csv, scipy
from math import pi
from scipy import sqrt, arctan2, arcsin, arccos, sin, cos, dot

def flatten(L):
    if isinstance(L, list): return [] if L == [] else flatten(L[0]) + flatten(L[1:])
    else: return [L]

def main():
    columns = ["HEAD", "NECK", "TORSO", "LEFT_SHOULDER", "LEFT_ELBOW", "RIGHT_SHOULDER", "RIGHT_ELBOW"]
    reader = csv.reader(sys.stdin)
    header = parse_header(reader.next())

    writer = csv.writer(sys.stdout)
    writer.writerow(flatten([[column + "_" + label for label in ["X", "Y", "Z"]] for column in columns]))
    for row in reader:
        matrixes = dict([(column, scipy.array([float(x) for x in row[header[column]:(header[column]+9)]]).reshape(3,3)) for column in columns])
        converted = convert_absolute_to_relative(matrixes)
        writer.writerow(flatten([matrix_to_angle(converted[column]) for column in columns]))

def parse_header(header):
    columns = {}
    for i in range(len(header)): columns[header[i]] = i + 5
    del columns['']
    return columns

def convert_absolute_to_relative(matrixes):
    converted = {}
    converted["TORSO"] = matrixes["TORSO"]
    invTorso = matrixes["TORSO"].transpose()
    converted["NECK"] = dot(invTorso, matrixes["NECK"])
    invNeck = converted["NECK"].transpose()
    converted["HEAD"] = dot(invNeck, matrixes["HEAD"])
    converted["LEFT_SHOULDER"] = dot(invNeck, matrixes["LEFT_SHOULDER"])
    converted["LEFT_ELBOW"] = dot(converted["LEFT_SHOULDER"], matrixes["LEFT_ELBOW"])
    converted["RIGHT_SHOULDER"] = dot(invNeck, matrixes["RIGHT_SHOULDER"])
    converted["RIGHT_ELBOW"] = dot(converted["RIGHT_SHOULDER"], matrixes["RIGHT_ELBOW"])
    return converted

def matrix_to_angle(m):
    y = arcsin(-m[2, 0])
    x = arctan2(m[2, 1], m[2, 2])
    z = arctan2(m[1, 0], m[0, 0])
    return [x, y, z]

if __name__ == "__main__":
    main()
