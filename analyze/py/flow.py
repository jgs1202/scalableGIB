# -*- coding: utf-8 -*-

import math
import os
import sys
import json
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas.tools.plotting as plotting


def calcFlow(trajes, abst):
    matrixes = [[[] for j in range(120)] for i in range(4)]
    for task in range(4):
        for que in range(120):
            total = 0
            groupSize = abst[task][que]['groupSize']
            matrix = np.zeros((groupSize, groupSize))
            for member in range(len(trajes[task][que])):
                for flow in range(len(trajes[task][que][member]) - 1):
                    src = trajes[task][que][member][flow]['AOI']
                    target = trajes[task][que][member][flow + 1]['AOI']
                    # if int(src) == int(target):
                    #     print('same points')
                    matrix[int(src) - 1][int(target) - 1] += 1
                    total += 1
            matrix = matrix / total * 100
            matrixes[task][que] = matrix
    return matrixes


def makefile():
    totalData = [[[] for j in range(120)] for i in range(4)]
    global origin, outpath, srcpath
    origin = '../src/Analyze/'
    outpath = '../src/trajectory/'
    srcpath = '../src/data/'

    data = json.load(open('../src/trajectory/fixations.json'))
    abst_data = json.load(open('../src/trajectory/abst_info.json'))
    matrixes = calcFlow(data, abst_data)
    print(len(matrixes[0]))

    for task in range(len(matrixes)):
        for matrix in range(len(matrixes[task])):
            row = ['AOI ' + str(i) for i in range(len(matrixes[task][matrix]))]
            column = ['AOI ' + str(i) for i in range(len(matrixes[task][matrix]))]
            fig, ax = plt.subplots(1, 1)
            table = plotting.table(ax, pd.DataFrame(matrixes[task][matrix]), rowLabels=row, colLabels=column, loc='center')
            table.scale(1, 1)
            # plt.title(out["name"])
            plt.close()
            ax.axis('off')
            f = open('../src/flows/task' + str(task + 1) + '/' + str(matrix) + '.json', 'w')
            json.dump(matrixes[task][matrix].tolist(), f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
            f.close()


def main():
    makefile()


if __name__ == '__main__':
    main()