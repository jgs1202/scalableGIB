# -*- coding: utf-8 -*-

import os
import math
import csv
import json
from statistics import mean, stdev
import copy


def main():
    data = json.load(open('../flaski/choice.json'))
    dic = {}
    dic['correct'] = 0
    dic['time'] = []
    error = 0
    out = [[copy.deepcopy(dic) for j in range(120)] for i in range(4)]
    for datum in data:
        task = int(datum['task']) - 1
        que = int(datum['file'][:-5])
        out[task][que]['correct'] += int(datum['answer'])
        out[task][que]['time'].append(int(datum['time']))
        out[task][que]['layout'] = datum['layout']
    for i in range(4):
        for j in range(120):
            # print(out[i][j]['correct'])
            print(len(out[i][j]['time']))
            out[i][j]['meanTime'] = mean(out[i][j]['time'])
            out[i][j]['totalTime'] = sum(out[i][j]['time'])
            out[i][j]['devTime'] = stdev(out[i][j]['time'])
            out[i][j]['people'] = len(out[i][j]['time'])
            del out[i][j]['time']
    f = open('../src/trajectory/perQuestion.json', 'w')
    json.dump(out, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
