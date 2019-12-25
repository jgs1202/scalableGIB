# -*- coding: utf-8 -*-

import numpy as np
import os
import csv
import sys
import json
import matplotlib.pyplot as plt


def main():
    data = json.load(open('../src/trajectory/fixation_detail.json', 'r'))
    outpath = '../src/trajectory/'
    outputs = [[[] for que in range(120)] for task in range(4)]
    tasknum = 0

    for task in range(4):
        for que in range(120):
            src_data = json.load(open('../src/data/task' + str(task + 1) + '/' + str(que) + '.json', 'r'))
            groupSize = src_data['groupSize']
            outputs[task][que] = [np.zeros(1000) for i in range(groupSize)]

            for datum in data[task][que]:
                AOIs = np.zeros(1000)
                segStart = int(datum['segmentStart'])
                segEnd = int(datum['segmentEnd'])
                duration = segEnd - segStart
                fixation = 0
                for step in range(1000):
                    gazeStart = float(datum['fixations'][fixation]['recStart'])
                    gazeDur = float(datum['fixations'][fixation]['gazeDur'])
                    if step * duration / 1000 + segStart > gazeStart + gazeDur:
                        fixation += 1
                        if fixation >= len(datum['fixations']):
                            break
                    if step * duration / 1000 + segStart >= gazeStart and step * duration / 1000 + segStart < gazeStart + gazeDur:
                        AOIs[step] = datum['fixations'][fixation]['AOI']
                for step in range(1000):
                    if int(AOIs[step]) == 0:
                        continue
                    outputs[task][que][int(AOIs[step]) - 1][step] += 1
            outputs[task][que] /= np.amax(outputs[task][que])
            outputs[task][que] = outputs[task][que].tolist()

    f = open(outpath + 'timeSeriesePlotData.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))           


if __name__ == '__main__':
    main()
