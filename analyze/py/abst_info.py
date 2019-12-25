# -*- coding: utf-8 -*-

import numpy as np
import os
import csv
import sys
import json
import matplotlib.pyplot as plt
import copy


def get_answer(data, task, que):
    if task == 0:
        return None
    elif task == 1:
        if que < 60:
            return [data['nodeMax'], data['node2ndMax'], data['node3rdMax']]
        else:
            return [data['nodeMin'], data['node2ndMin'], data['node3rdMin']]
    elif task == 2:
        if que < 60:
            return [data['linkMax'], data['link2ndMax'], data['link3rdMax']]
        else:
            return [data['linkMin'], data['link2ndMin'], data['link3rdMin']]
    elif task == 3:
        return [data['linkOutMost'], data['linkOut2nd'], data['linkOut3rd']]


def main():
    ref_path = '../src/data/'
    origin_data = json.load(open('../src/trajectory/abst_info.json', 'r'))
    result = json.load(open('../src/trajectory/perQuestion.json', 'r'))
    outputs = copy.deepcopy(origin_data)

    for task in range(4):
        for que in range(120):
            data = json.load(open(ref_path + 'task' + str(task + 1) + '/' + str(que) + '.json', 'r'))
            answers = get_answer(data, task, que)
            if type(answers) == list:
                if type(answers[0]) == list:
                    answers[0] = answers[0][0]
            outputs[task][que]['correct'] = result[task][que]['correct']
            outputs[task][que]['people'] = result[task][que]['people']
            outputs[task][que]['meanTime'] = result[task][que]['meanTime']
            outputs[task][que]['devTime'] = result[task][que]['devTime']
            outputs[task][que]['answers'] = answers

    outpath = '../src/trajectory/'
    f = open(outpath + 'queInfo.json', 'w')
    json.dump(outputs, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))           


if __name__ == '__main__':
    main()
