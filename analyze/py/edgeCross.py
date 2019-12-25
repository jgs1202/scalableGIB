# -*- coding: utf-8 -*-

# size is 900*600

import json
import os
import math
import numpy as np
from itertools import combinations
from statistics import mean, stdev
import community
import networkx as nx
from networkx.readwrite import json_graph


def edgeCross(data):
    nodes = [(node['cx'], node['cy']) for node in data['nodes']]
    links = [(link['source'], link['target']) for link in data['links']]
    total = 0
    angle = []

    for (index1, index2), (index3, index4) in combinations(links, 2):
        sx1, sy1 = nodes[index1]
        tx1, ty1 = nodes[index2]
        sx2, sy2 = nodes[index3]
        tx2, ty2 = nodes[index4]

        # if an either of thw two links is vertical, we do not count
        if tx1 == sx1 and tx2 != sx2:
            x = tx1
            y = (ty2 - sy2) / (tx2 - sx2) * (x - sx2) + sy2
        elif tx1 != sx1 and tx2 == sx2:
            x = tx2
            y = (ty1 - sy1) / (tx1 - sx1) * (x - sx1) + sy1
        else:
            tan1 = (ty1 - sy1) / (tx1 - sx1)
            tan2 = (ty2 - sy2) / (tx2 - sx2)
            # tan1 * x - tan1 * sx1 + sy1 = tan2 * x - tan2 * sx2 + sy2
            if tan1 == tan2:
                x = False
                y = False
            else:
                x = (sy2 - sy1 + tan1 * sx1 - tan2 * sx2) / (tan1 - tan2)
                y = tan1 * (x - sx1) + sy1
        # if intersection point is same as either of source or target we do not count
        if x == sx1 and y == sy1:
            continue
        if x == sx2 and y == sy2:
            continue
        if x == tx1 and y == ty1:
            continue
        if x == tx2 and y == ty2:
            continue
        if (sx1 > x and tx1 > x) or (sx1 < x and tx1 < x):
            continue
        if (sx2 > x and tx2 > x) or (sx2 < x and tx2 < x):
            continue
        if (sy1 > y and ty1 > y) or (sy1 < y and ty1 < y):
            continue
        if (sy1 > y and ty1 > y) or (sy1 < y and ty1 < y):
            continue
        total += 1
        # print('tan1, tan2 is')
        # print(tan1, tan2)
        # print('1, 2 is')
        # print(np.arctan(tan1), np.arctan(tan2))
        tmp = abs(np.arctan(tan1) - np.arctan(tan2)) / math.pi * 180
        if tmp > 90:
            tmp = 180 - tmp
        angle.append(tmp)
    return angle


def getStatic(data):
    list = []
    for i in range(len(data)):
        if i != 0:
            data[i][1] = int(data[i][1])
            data[i][2] = float(data[i][2])
            data[i][3] = float(data[i][3])
            data[i][4] = float(data[i][4])
            data[i][5] = float(data[i][5])
            data[i][6] = float(data[i][6])
            data[i][7] = float(data[i][7])
            data[i][8] = int(data[i][8])
            # data[i][9] = float(data[i][9])
        if data[i][0] == 'FDGIB':
            data[i][5] = 1.0
    for i in data:
        if i[0] != 'type':
            dic = {}
            dic['type'], dic['groupSize'], dic['pgroup'], dic['pout'], dic['edgeCross'], dic['meanAspect'], dic['meanSpaceWasted'], dic['meanModularity'], dic['linkSize'], dic['edgeLength'] = i[0], [], i[2], i[3],[],[],[],[],[], []
            if dic not in list:
                list.append(dic)
    for datum in data:
        for i in range(len(list)):
            # print(datum[0], list[i]['type'], datum[1], list[i]['groupSize'], datum[2], list[i]['pgroup'], datum[3], list[i]['pout'], )
            if datum[0] == list[i]['type']:
                print(datum[0])
                list[i]['groupSize'].append(datum[1])
                list[i]['edgeCross'].append(datum[4])
                list[i]['meanAspect'].append(datum[5])
                list[i]['meanSpaceWasted'].append(100 - datum[6] * 100)
                list[i]['meanModularity'].append(datum[7])
                list[i]['linkSize'].append(datum[8])
                list[i]['edgeLength'].append(datum[9])
                if 'total' in list[i].keys():
                    list[i]['total'] += 1
                else:
                    list[i]['total'] = 1
    for i in range(len(list)):
        # try:
        #     list[i]['nodeSize'] /= list[i]['total']
        #     list[i]['linkSize'] /= list[i]['total']
        # except:
        #     print('total is zero')
        list[i]['groupSize'] = mean(list[i]['groupSize'])
        list[i]['devlink'] = stdev(list[i]['linkSize'])
        list[i]['linkSize'] = mean(list[i]['linkSize'])
        # list[i]['devEdgeCross'] = stdev(list[i]['edgeCross'])
        # list[i]['edgeCross'] = mean(list[i]['edgeCross'])
        # list[i]['devAspect'] = stdev(list[i]['meanAspect'])
        # list[i]['meanAspect'] = mean(list[i]['meanAspect'])
        # list[i]['devSpaceWasted'] = stdev(list[i]['meanSpaceWasted'])
        # list[i]['meanSpaceWasted'] = mean(list[i]['meanSpaceWasted'])
        # list[i]['meanModularity'] = mean(list[i]['meanModularity'])
        for j in range(len(list[i]['edgeLength'])):
            for k in range(len(list[i]['edgeLength'][j])):
                list[i]['edgeLength'][j][k] /= mean(list[i]['meanSpaceWasted']) / 100
            list[i]['edgeLength'][j] = stdev(list[i]['edgeLength'][j])
        # list[i]['devLength'] = stdev(list[i]['edgeLength'])
        # list[i]['edgeLength'] = mean(list[i]['edgeLength'])
    f = open('../data/result.json', 'w')
    json.dump(list, f, ensure_ascii=False, indent=4, sort_keys=True, separators= (',', ': '))


def verify_layout(str):
    if str == 'STGIB':
        return 0
    elif str == 'Chaturvedi':
        return 1
    elif str == 'FDGIB':
        return 2
    elif str == 'TRGIB':
        return 3


if __name__ == '__main__':
    pathes = []
    pathes.append('../src/data/task1/')
    pathes.append('../src/data/task2/')
    pathes.append('../src/data/task3/')
    pathes.append('../src/data/task4/')
    output = [{"data": []} for i in range(4)]
    output[0]['layout'] = 'ST-GIB'
    output[1]['layout'] = 'Chaturvedi'
    output[2]['layout'] = 'FD-GIB'
    output[3]['layout'] = 'TR-GIB'

    for path in pathes:
        for file in os.listdir(path):
            if file != '.DS_Store':
                # if file == '0.json' or file=='1.json'or file=='2.json':
                    # print(file)
                    data = json.load(open(path + file, 'r'))
                    layout = data['layout']
                    print(layout)
                    list = []
                    angle = edgeCross(data)
                    # print(angle)
                    output[verify_layout(layout)]['data'].extend(angle)
    for i in output:
        print(i['layout'], mean(i['data']), stdev(i['data']))
    f = open('../flaski/angle.json', 'w')
    json.dump(output, f, ensure_ascii=False, indent=4, sort_keys=True, separators= (',', ': '))


    #ST-GIB 64.87612341558717 34.52025256078577
    #Chaturvedi 64.79478709353492 34.66007070156563
    #FD-GIB 68.79001399746704 36.43641685076299
    #TR-GIB 65.03138378772711 34.855267580831175
