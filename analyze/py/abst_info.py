# -*- coding: utf-8 -*-

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
    fd_index = [[], []]
    fd_files = [[], []]

    for que in range(total):
        graph = json.load(open('../../src/data/random/' + str(que) + '.json', 'r'))
        layout, level, file = question_info(graph)

        if layout == 1:
            outputs[que] = data[layout][level][file]
        if layout == 0:
            fd_index[level].append(que)
            fd_files[level].append(file)

    fd_sorted = [sorted(fd_files[0]), sorted(fd_files[1])]
    for level in range(2):
        for que in range(len(fd_index[level])):
            file = fd_sorted[level].index(fd_files[level][que])
            outputs[fd_index[level][que]] = data[0][level][file]

    f = open('../data/abst_info.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    f = open('../../src/data/eye-tracking/abst_info.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
