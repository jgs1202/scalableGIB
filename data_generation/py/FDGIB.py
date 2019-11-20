# -*- coding: utf-8 -*-

import os
import math
import json
import networkx as nx
from PRISM import main as prism
from statistics import mean
import matplotlib.pyplot as plt


def force(data, width, height, groups):
    G = nx.Graph()
    length = int(data['groupSize'])
    G.add_nodes_from([i for i in range(length)])
    # G.add_node(length)
    # for i in range(length):
    #     G.add_edge(i, length)
    # calculate the number of links in each group
    linkNum = count_link(data)
    for i in range(len(linkNum)):
        for j in range(len(linkNum[i])):
            if linkNum[i][j] != 0:
                G.add_edge(i, i + j + 1, weight=linkNum[i][j])

    plt.figure(figsize=(9.6, 6))
    pos = nx.spring_layout(G, k=1/len(data['nodes']))
    nx.draw_networkx(G, pos)
    plt.ylim(1, -1)
    plt.show()
    nx.draw(pos, node_color='b', node_size=50, with_labels=False)

    xs, ys = [], []
    for i in range(length):
        temp = pos[i]
        xs.append(temp[0])
        ys.append(temp[1])
    for i in range(length):
        pos[i] *= 200
        pos[i][0] += 450
        pos[i][1] += 300

    ################################### width * height boxへの対応
    area = width * height * 0.2
    unit = area / len(data['nodes'])
    for i in range(length):
        # print(i, length)
        data['groups'][i]['dx'] = math.sqrt(unit * len(groups[i]))
        data['groups'][i]['dy'] = data['groups'][i]['dx']
        data['groups'][i]['x'] = pos[i][0]
        data['groups'][i]['y'] = pos[i][1]

    # import pylab as pl
    # pl.xticks([0, width])
    # pl.yticks([0, height])
    # for i in data['groups']:
    #     pl.gca().add_patch(pl.Rectangle(xy=[i['x'], height - i['y']], width=i['dx'], height=i['dy'], linewidth='1.0', fill=False))
    # pl.show()

    data = prism(data, linkNum, width, height)
    return data


def count_link(data):
    max = 0
    for i in data['nodes']:
        if i['group'] > max:
            max = i['group']
    boxNum = max + 1
    linkNum = []
    for i in range(boxNum):
        linkNum.append([])
        for j in range(boxNum - i):
            linkNum[i].append(0)
    links = data['links']

    for i in links:
        source = data['nodes'][i['source']]['group']
        target = data['nodes'][i['target']]['group']
        if source != target:
            if source < target:
                if linkNum[source][target - source] == 0:
                    linkNum[source][target - source] = 1
                else:
                    linkNum[source][target - source] += 1
            else:
                if linkNum[target][source - target] == 0:
                    linkNum[target][source - target] = 1
                else:
                    linkNum[target][source - target] += 1
    return linkNum


if __name__ == '__main__':
    data = 1
    dir = '../data/origin/FDGIB/high-mid/'
    for i in os.listdir(dir):
        if i[-5:] == '.json':
            data = json.load(open(dir + i))

    groups = [[] for i in range(data['groupSize'])]
    length = len(data['nodes'])
    nodes = data['nodes']
    for i in range(data['groupSize']):
        dic = {}
        dic['number'] = i
        groups[nodes[i]['group']].append(dic)

    force(data, 960, 600, groups)
