import random
import math
from operator import itemgetter
import json
import os
import sys
import numpy as np


def max_link():
    return 100


def p_group(groupsize, nodesize):
    def index(groupsize):
        if groupsize < 11.4:
            return 0
        else:
            return (groupsize - 11.4) / 15
    return 0.2 * math.exp(-index(groupsize))


def p_in(groupsize, nodesize):
    def index(nodesize):
        if nodesize < 30:
            return 0
        else:
            return (nodesize - 30) / 50
    return 0.286 * 0.3 * math.exp(-index(nodesize))


def p_bridge(groupsize):
    def index(groupsize):
        if groupsize < 11.4:
            return 0
        else:
            return (groupsize - 11.4) / 20
    return 0.05 * 0.3 * math.exp(-index(groupsize))


def p_out(groupsize, nodesize):
    def index(groupsize, nodesize):
        if groupsize * nodesize < 11.4 * 30:
            return 0
        else:
            return (groupsize * nodesize - 11.4 * 30) / 11.4 * 30
    return 0.05 * 0.3 * math.exp(-index(groupsize, nodesize))

def makeData():
    eachNum = 5
    output = ['TRGIB', 'FDGIB']
    nodelevels = ['low', 'mid', 'high']
    nodeSizes = [10, 50, 100]
    grouplevels = ['low', 'mid', 'high']
    groupSizes = [5, 20, 40]
    thre = 0.3
    nodeThre = 0.4
    pin = 0.286
    pbridge = 0.05
    # mset = [7, 14, 14]
    pgroup = 0.2
    # poutset = [0, 0.001, 0.002]
    pout = 0.002
    nodemean = 52.5
    nodestdev = 35.3

    pin = pin * thre
    pbridge = round(pbridge * thre, 4)
    # pgroup = round(pgroup * thre, 3)
    pout = round(pout * thre, 5)

    for layout in range(len(output)):
        print('step = ' + str(layout))
        for nodelevel in range(len(nodelevels)):
            for grouplevel in range(len(grouplevels)):
                for each in range(eachNum):
                    # print(layout, nodelevel, grouplevel, each)
                    # verify = False
                    # while verify is False:
                    m = groupSizes[grouplevel]
                    nodes = []
                    links = []
                    total = 0
                    num = 0
                    linkid = 0

                    for l in range(m):
                        nodes.append([])

                    for l in range(m):
                        # rand = random.randint(nmin, nmax)
                        rand = 0
                        nodesize = nodeSizes[nodelevel]
                        while rand < 4 / nodeThre or rand > nodesize + nodesize / 2:
                            rand = np.random.normal(nodesize, nodesize, 1)[0]
                            # rand *= nodeThre
                        if rand < 4:
                            rand = 4
                        try:
                            rand = round(rand).astype(np.int32)
                        except:
                            rand = int(rand)
                        for j in range(rand):
                            nodes[l].append(num)
                            num += 1

                    for l in range(m):
                        length = len(nodes[l])
                        total += len(nodes[l])
                        for j in range(length):
                            for k in range(length - j - 1):
                                pin = 0
                                while pin < 0.186 or pin > 0.386:
                                    pin = np.random.normal(0.286, 0.1, 1)[0]
                                pin *= thre
                                pin = p_in(m, nodesize)
                                if random.random() < pin:
                                    dic = {}
                                    dic['source'] = nodes[l][j]
                                    dic['target'] = nodes[l][j + k + 1]
                                    dic['value'] = 1
                                    dic['id'] = linkid
                                    linkid += 1
                                    links.append(dic)


                    for p in range(m):
                        length1 = len(nodes)
                        length2 = len(nodes[p])
                        for j in range(length1 - p - 1):
                            if random.random() < p_group(m, nodesize):
                                length3 = len(nodes[p + j + 1])
                                for k in range(length2):
                                    for l in range(length3):
                                        if random.random() < p_bridge(m):
                                            dic = {}
                                            dic['source'] = nodes[p][k]
                                            dic['target'] = nodes[p + j + 1][l]
                                            dic['value'] = 1
                                            dic['id'] = linkid
                                            linkid += 1
                                            links.append(dic)

                    for p in range(m):
                        links.sort(key=itemgetter('source'))

                    current = 0
                    for p in range(total):
                        for j in range(total - p - 1):
                            if current == len(links):
                                break
                            elif links[current]['source'] == p and links[current]['target'] == p + j + 1:
                                current += 1
                            else:
                                if random.random() < p_out(m, nodesize):
                                    dic = {}
                                    dic['source'] = p
                                    dic['target'] = p + j + 1
                                    dic['value'] = 1
                                    dic['id'] = linkid
                                    linkid += 1
                                    links.append(dic)
                                    current += 1

                    nodes_for_write = []
                    length = len(nodes)
                    for p in range(length):
                        lengthG = len(nodes[p])
                        for j in range(lengthG):
                            dic = {}
                            dic['name'] = nodes[p][j]
                            dic['id'] = nodes[p][j]
                            dic['group'] = p
                            nodes_for_write.append(dic)

                    data = {}
                    data['groups'] = [{} for i in range(m)]
                    data['groupSize'] = m
                    data['grouplevel'] = grouplevels[grouplevel]
                    data['nodelevel'] = nodelevels[nodelevel]
                    data['pgroup'] = pgroup
                    data['pout'] = pout
                    data['nodes'] = nodes_for_write
                    data['linkSize'] = len(links)
                    data['nodeSize'] = len(nodes_for_write)
                    data['links'] = links
                    data['file'] = str(each) + '.json'
                    data['dir'] = str(m) + '-' + str(pgroup) + '-' + str(pout)
                    data = calc(data, m)

                    if not os.path.exists('../data/origin/' + output[layout] + '/' + grouplevels[grouplevel] + '-' + nodelevels[nodelevel]):
                        os.mkdir('../data/origin/' + output[layout] + '/' + grouplevels[grouplevel] + '-' + nodelevels[nodelevel])

                    # if len(data['mostConnected']) == 1:
                    #     try:
                    #         data['linkMax']
                    #         data['linkMin']
                    #         data['nodeMax']
                    #         data['nodeMin']
                    #         verify = True
                    f = open('../data/origin/' + output[layout] + '/' + grouplevels[grouplevel] + '-' + nodelevels[nodelevel] + '/' + str(each) + '.json', 'w')
                    intM = 0
                    for p in range(m + 1):
                        if p == m:
                            intM = p
                    data['groupSize'] = intM

                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
                    # except:
                    #     pass
                # f = open('../data/links.json', 'w')
                # json.dump(links, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def calc(data, m):
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
    # print(len(links))
    for i in links:
        # print(i)
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

    max = linkNum[0][0]
    most = []
    for i in range(len(linkNum)):
        for j in range(len(linkNum[i])):
            if linkNum[i][j] > max:
                most = [[i, i + j]]
                max = linkNum[i][j]
            elif linkNum[i][j] == max:
                most.append([i, i + j])

    # print(most)
    data['mostConnected'] = most

    linkGroup = [[i, 0] for i in range(m)]
    nodeGroup = [[i, 0] for i in range(m)]
    for i in data['nodes']:
        nodeGroup[i['group']][1] += 1
    for i in data['links']:
        srcGroup = data['nodes'][i['source']]['group']
        tarGroup = data['nodes'][i['target']]['group']
        if srcGroup == tarGroup:
            linkGroup[srcGroup][1] += 1
    linkGroup.sort(key=itemgetter(1), reverse=True)
    nodeGroup.sort(key=itemgetter(1), reverse=True)
    if nodeGroup[0][1] > nodeGroup[1][1]:
        data['nodeMax'] = nodeGroup[0][0]
    if nodeGroup[-1][1] < nodeGroup[-2][1]:
        data['nodeMin'] = nodeGroup[-1][0]
    if linkGroup[0][1] > linkGroup[1][1]:
        data['linkMax'] = linkGroup[0][0]
    if linkGroup[-1][1] < linkGroup[-2][1]:
        data['linkMin'] = linkGroup[-1][0]
    # print(linkGroup[0][0], data['linkMax'])
    # sys.exit()
    return data

if __name__ == '__main__':
    makeData()
    cmds = ['python groupWeight.py']
    for i in cmds:
        cmd = i
    os.system(cmd)
