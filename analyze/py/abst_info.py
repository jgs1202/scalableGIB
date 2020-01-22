# -*- coding: utf-8 -*-

#lack of fd is easy: 4, hard: 2, 4, 14, 21

import numpy as np
import os
import csv
import sys
import json
import matplotlib.pyplot as plt
import copy


def question_info(graph):
    layout, level, file = 0, 0, 0

    if graph['layout'] == 'FDGIB':
        layout = 0
    else:
        layout = 1
    if graph['groupSize'] == 10:
        level = 0
    elif graph['groupSize'] == 40:
        level = 1
    try:
        file = int(graph['file'][:2])
    except:
        file = int(graph['file'][0])

    return layout, level, file


def main():
    total = 120
    data = json.load(open('../data/perQuestion.json', 'r'))
    outputs = [{} for i in range(total)]

    for que in range(total):
        graph = json.load(open('../../src/data/random/' + str(que) + '.json', 'r'))
        layout, level, file = question_info(graph)

        if layout == 1:
            outputs[que] = data[layout][level][file]
        if layout == 0:
            # fd_index[level].append(que)
            # fd_files[level].append(file)
            if file >= 30:
                if file == 30:
                    file = 4
                if file == 31:
                    file = 2
                if file == 32:
                    file = 14
                if file == 33:
                    file = 21
            outputs[que] = data[layout][level][file]

    f = open('../data/abst_info.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    f = open('../../src/data/eye-tracking/abst_info.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
