#!/usr/bin/env python

import sys, csv, scipy
from math import pi
from scipy import sqrt, arctan2, arcsin, arccos, sin, cos, dot

def flatten(L):
    if isinstance(L, list):
        if L == []:
            return []
        else:
            return flatten(L[0]) + flatten(L[1:])
    else:
        return [L]

def main():
    COLUMNS = { "HEAD": 6, "NECK": 20, "TORSO": 34,
                "LEFT_SHOULDER": 48, "LEFT_ELBOW": 62,
                "RIGHT_SHOULDER": 90, "RIGHT_ELBOW": 104 }
    AXES = ["X", "Y", "Z"]
    data = []

    header = []
    for key in sorted(COLUMNS.keys()):
        header.extend(map(lambda a: key + "_" + a, AXES))
    data.append(header)
    
    reader = csv.reader(sys.stdin)
    reader.next()
    for line in reader:
        matrixes = dict(map((lambda(joint, column): 
                             (joint, scipy.array(map((lambda x: float(x)), line[column : (column + 9)])).reshape(3, 3))),
                            COLUMNS.items()))
        data.append(flatten(map(lambda(key, val): convert_matrix_to_angle(val), sorted(convert_world_to_local(matrixes).items()))))

    fix_jump(data)    
    csv.writer(sys.stdout).writerows(data)

def convert_world_to_local(joint_matrix):
    converted_matrix = {}
    converted_matrix["TORSO"] = joint_matrix["TORSO"]
    invTorso = joint_matrix["TORSO"].transpose()
    converted_matrix["NECK"] = dot(invTorso, joint_matrix["NECK"])
    invNeck = converted_matrix["NECK"].transpose()
    converted_matrix["HEAD"] = dot(invNeck, joint_matrix["HEAD"])
    converted_matrix["LEFT_SHOULDER"] = dot(invNeck, joint_matrix["LEFT_SHOULDER"])
    converted_matrix["LEFT_ELBOW"] = dot(converted_matrix["LEFT_SHOULDER"], joint_matrix["LEFT_ELBOW"])
    converted_matrix["RIGHT_SHOULDER"] = dot(invNeck, joint_matrix["RIGHT_SHOULDER"])
    converted_matrix["RIGHT_ELBOW"] = dot(converted_matrix["RIGHT_SHOULDER"], joint_matrix["RIGHT_ELBOW"])
    return converted_matrix

def convert_matrix_to_angle(m):
    y = arcsin(-m[2, 0])
    x = arctan2(m[2,1], m[2,2])
    z = arctan2(m[1,0], m[0,0])
    return [x, y, z]

def fix_jump(data):
    column_len = len(data[0])
    prev =  data[1]
    for row in data[2:]:
        for i in range(column_len):
            sign = row[i] * prev[i]
            diff = abs(row[i] - prev[i])
            if( sign < 0 and diff > pi * 1.8):
                if(diff > pi * 2):
                    row[i] = -row[i]
                else:
                    row[i] = 2 * pi + row[i] if(prev[i] > 0) else -2 * pi + row[i]
        prev = row

if __name__ == "__main__":
    main()
