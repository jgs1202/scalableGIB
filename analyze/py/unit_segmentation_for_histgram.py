# -*- coding: utf-8 -*-

import numpy as np
import os
import csv
import sys
import json
import matplotlib.pyplot as plt


def main():
    data = json.load(open('../data/fixation_detail.json', 'r'))
    total_que = 120
    total_step = 1000
    outputs = [[] for que in range(total_que)]

    for que in range(total_que):
        src_data = json.load(open('../../src/data/random/' + str(que) + '.json', 'r'))
        groupSize = src_data['groupSize']
        outputs[que] = [np.zeros(total_step) for i in range(groupSize)]

        for datum in data[que]:
            AOIs = np.zeros(total_step)
            segStart = int(datum['segmentStart'])
            segEnd = int(datum['segmentEnd'])
            duration = segEnd - segStart

            fixation = 0
            for step in range(total_step):
                gazeStart = float(datum['fixations'][fixation]['recStart'])
                gazeDur = float(datum['fixations'][fixation]['gazeDur'])
                if step * duration / 1000 + segStart > gazeStart + gazeDur:
                    fixation += 1
                    if fixation >= len(datum['fixations']):
                        break
                if step * duration / 1000 + segStart >= gazeStart and step * duration / 1000 + segStart < gazeStart + gazeDur:
                    AOIs[step] = datum['fixations'][fixation]['AOI']
            for step in range(total_step):
                if int(AOIs[step]) >= 0:
                    outputs[que][int(AOIs[step])][step] += 1
        outputs[que] /= np.amax(outputs[que])
        outputs[que] = outputs[que].tolist()

    f = open('../data/timeSeriesePlotData.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f = open('../../src/data/eye-tracking/timeSeriesePlotData.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
