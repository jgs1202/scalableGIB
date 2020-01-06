# -*- coding: utf-8 -*-

import os
import math
import csv
import json
from statistics import mean, stdev
import copy


def layout_num(layout):
    if layout == 'FDGIB':
        return 0
    elif layout == 'TRGIB':
        return 1


def level_num(groupSize):
    groupSize = int(groupSize)
    if groupSize == 10:
        return 0
    elif groupSize == 40:
        return 1


def FD_index():
    path = '../../src/data/random/'
    total = 120
    index = [[], []]
    for que in range(total):
        data = json.load(open(path + str(que) + '.json'))
        if data['layout'] == 'FDGIB':
            level = level_num(data['groupSize'])
            index[level].append(int(data['file'][:-5]))
    index = [sorted(i) for i in index]
    return index


def main(fd_index):
    limit_second = 30 * 1000
    each_que = 30
    each_layout = 2
    each_level = 2
    data = json.load(open('../data/choice.json'))
    dic = {}
    dic['correct'] = 0
    dic['time'] = []
    out = [[[copy.deepcopy(dic) for j in range(each_que)] for i in range(each_level)] for k in range(each_layout)]
    dic = {}
    dic['answer'] = []
    dic['all_time'] = []
    dic['correct_time'] = []
    out_answers = [[copy.deepcopy(dic) for i in range(each_level)] for k in range(each_layout)]
    out_alldata = [[[[] for j in range(each_que)] for i in range(each_level)] for k in range(each_layout)]

    for datum in data:
        layout = int(layout_num(datum['layout']))
        level = level_num(datum['groupSize'])
        que = int(datum['origin_file'][:-5])
        if layout == 0:
            que = fd_index[level].index(que)
        out[layout][level][que]['correct'] += int(datum['answer'])
        out[layout][level][que]['time'].append(int(datum['time']))
        out[layout][level][que]['layout'] = datum['layout']
        out[layout][level][que]['file'] = str(que) + '.json'
        out[layout][level][que]['layout'] = datum['layout']
        out[layout][level][que]['groupSize'] = datum['groupSize']
        out_alldata[layout][level][que].append(datum)
        out_answers[layout][level]['answer'].append(datum['answer'])
        out_answers[layout][level]['all_time'].append(datum['time'])
        if datum['answer'] == 1:
            out_answers[layout][level]['correct_time'].append(datum['time'])

    for layout in range(each_layout):
        for level in range(each_level):
            for que in range(each_que):
                if len(out[layout][level][que]) != 0:
                    correctTime = [time for time in out[layout][level][que]['time'] if time != limit_second]
                    if len(correctTime) != 0:
                        out[layout][level][que]['meanCorrectTime'] = mean(correctTime)
                    else:
                        out[layout][level][que]['meanCorrectTime'] = None
                    if len(correctTime) > 1:
                        out[layout][level][que]['devTime'] = stdev(correctTime)
                    else:
                        out[layout][level][que]['devTime'] = None
                    out[layout][level][que]['totalMeanTime'] = mean(out[layout][level][que]['time'])
                    out[layout][level][que]['people'] = len(out[layout][level][que]['time'])
            del out[layout][level][que]['time']
    f = open('../data/perQuestion.json', 'w')
    json.dump(out, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f = open('../data/allData.json', 'w')
    json.dump(out_alldata, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f = open('../data/answers.json', 'w')
    json.dump(out_answers, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    fd_index = FD_index()
    main(fd_index)
