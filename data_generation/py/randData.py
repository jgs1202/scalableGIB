import random
import math
from operator import itemgetter
import json
import os
import sys
import numpy as np
import random

threshold = 0.5


def max_link():
    return 100


def p_in(groupsize, nodesize, nodes_lenth):
    def index(nodesize):
        if nodesize < 30:
            return 0
        else:
            # return /(nodesize - 30) / 60
            return 0
    if nodes_lenth > 15:
        p = 0.15 * threshold
    else:
        p = 0.15 * 11.4 / (nodes_lenth - 2)
    # print(nodes_lenth, p)
    return p
    # return 0.4 * threshold


def p_group(groupsize, nodesize):
    return 0.1 * 11.4 / groupsize


def p_bridge(groupsize):
    return 0.04 * threshold


def p_out(groupsize, nodesize):
    p = 0.001 * 11.4 / groupsize * threshold
    if p > 0.05:
        return 0.05
    else:
        return p


def density(nodeNum, linkNum):
    return 2 * linkNum / (nodeNum * (nodeNum - 1))


def linear_density(nodeNum, linkNum):
    return linkNum / nodeNum


def inner_edge_ratio(nodes, links):
    count = 0
    for link in links:
        if nodes[link['source']]['group'] == nodes[link['target']]['group']:
            count += 1
    print('inner edge ratio is ' + str(round(count / len(links) * 100)))


def modify_density(nums, densityTwitter, links, nodes, m, nodesize):
    print(linear_density(nums[0], nums[1]), nums[0], nums[1])
    count = 0
    if linear_density(nums[0], nums[1]) < densityTwitter:
        while (abs(linear_density(nums[0], nums[1]) - densityTwitter) > 0.01):
            length = nums[0]
            rand = [random.randint(0, length - 1), random.randint(0, length - 1)]
            while rand[1] == rand[0]:
                rand[1] = random.randint(0, length - 1)
            flag = False
            for link in links:
                if (link['source'] == rand[0] and link['target'] == rand[1]) or (link['source'] == rand[1] and link['target'] == rand[0]):
                    flag = True
                    break
            if nodes[rand[0]]['group'] == nodes[rand[1]]['group']:
                if random.random() > p_in(m, nodesize, 30):
                    flag = True
            elif nodes[rand[0]]['group'] != nodes[rand[1]]['group']:
                if random.random() > p_out(m, nodesize):
                    flag = True
            if not flag:
                dic = {}
                dic['source'] = rand[0]
                dic['target'] = rand[1]
                dic['value'] = 1
                dic['id'] = nums[1]
                links.append(dic)
                nums[1] += 1

            # count += 1
            # if count % 10000 == 0:
            #     print(linear_density(nums[0], nums[1]))

    elif linear_density(nums[0], nums[1]) > densityTwitter:
        while (abs(linear_density(nums[0], nums[1]) - densityTwitter) > 0.01):
            # print(abs(linear_density(nums[0], nums[1]) - densityTwitter), nums[0], nums[1], len(links))
            rand = random.randint(0, len(links) - 1)
            link_id = links[rand]['id']
            link = links[rand]

            flag = False
            if nodes[link['source']]['group'] == nodes[link['target']]['group']:
                if random.random() < p_in(m, nodesize, 30):
                    flag = True
            elif nodes[link['source']]['group'] != nodes[link['target']]['group']:
                if random.random() < p_out(m, nodesize):
                    flag = True

            if not flag:
                del links[rand]
                for num in range(len(links)):
                    if links[num]['id'] > link_id:
                        links[num]['id'] = links[num]['id'] - 1
                nums[1] -= 1

            # count += 1
            # if count % 10000 == 0:
            #     print(linear_density(nums[0], nums[1]))


def nodes_writing(nodes):
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
    return nodes_for_write


def add_node(m, nodesize, nodes, nums):
    for l in range(m):
        rand = 0
        while rand < 4 or rand > nodesize + nodesize / 2:
            rand = np.random.normal(nodesize, nodesize, 1)[0]
        rand = int(rand)
        # print(rand)
        for j in range(rand):
            nodes[l].append(nums[0])
            nums[0] += 1


def add_link(m, nodes, links, nums, thre, nodesize):
    for l in range(m):
        length = len(nodes[l])
        for j in range(length):
            for k in range(length - j - 1):
                pin = p_in(m, nodesize, length)
                if random.random() < pin:
                    dic = {}
                    dic['source'] = nodes[l][j]
                    dic['target'] = nodes[l][j + k + 1]
                    dic['value'] = 1
                    dic['id'] = nums[1]
                    nums[1] += 1
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
                            dic['id'] = nums[1]
                            nums[1] += 1
                            links.append(dic)

    for p in range(m):
        links.sort(key=itemgetter('source'))

    current = 0
    for p in range(nums[0]):
        for j in range(nums[0] - p - 1):
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
                    dic['id'] = nums[1]
                    nums[1] += 1
                    links.append(dic)
                    current += 1


def makeData():
    eachNum = 40
    # nodelevels = ['low', 'mid', 'high']
    nodelevels = ['mid']
    nodeSizes = [20]
    # nodeSizes = [10, 50, 100]
    grouplevels = ['low', 'mid', 'high']
    groupSizes = [10, 20, 40]
    thre = 0.3
    nodeThre = 0.4
    pin = 0.286
    pbridge = 0.05
    pgroup = 0.2
    pout = 0.002
    nodemean = 52.5
    nodestdev = 35.3
    # linear_density = 0.0523
    densityTwitter = 2 * 7820.8 / (547.3 * (547.3 - 1))
    densityTwitter *= threshold
    densityTwitter = 1

    pin = pin * thre
    pbridge = round(pbridge * thre, 4)
    # pgroup = round(pgroup * thre, 3)
    pout = round(pout * thre, 5)

    for nodelevel in range(len(nodelevels)):
        for grouplevel in range(len(grouplevels)):
            for each in range(eachNum):
                m = groupSizes[grouplevel]
                nodes = [[] for i in range(m)]
                links = []
                nums = [0, 0]
                nodesize = nodeSizes[nodelevel]

                add_node(m, nodesize, nodes, nums)
                nodes_for_write = nodes_writing(nodes)
                add_link(m, nodes, links, nums, thre, nodesize)
                modify_density(nums, densityTwitter, links, nodes_for_write, m, nodesize)
                inner_edge_ratio(nodes_for_write, links)

                data = {}
                data['groups'] = [{} for i in range(m)]
                data['groupSize'] = m
                data['grouplevel'] = grouplevels[grouplevel]
                data['nodelevel'] = nodelevels[nodelevel]
                data['nodes'] = nodes_for_write
                data['linkSize'] = len(links)
                data['nodeSize'] = len(nodes_for_write)
                data['links'] = links
                data['level'] = grouplevels[grouplevel] + '-' + nodelevels[nodelevel]
                data['file'] = str(each) + '.json'
                if not os.path.exists('../data/origin/' + grouplevels[grouplevel] + '-' + nodelevels[nodelevel]):
                    os.mkdir('../data/origin/' + grouplevels[grouplevel] + '-' + nodelevels[nodelevel])
                f = open('../data/origin/' + grouplevels[grouplevel] + '-' + nodelevels[nodelevel] + '/' + str(each) + '.json', 'w')
                json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


def delete_directries():
    path = '../data/origin/'
    for layout in os.listdir(path):
        if layout != ".DS_Store":
            layout += '/'
            for level in os.listdir(path + layout):
                os.system('rm -r ' + path + layout + level)


def delete_temp():
    layouts = ['../data/FDGIB/', '../data/TRGIB/']
    for layout in layouts:
        path = layout + 'temp/'
        for file in os.listdir(path + file):
            if file != 'DS_Store':
                os.system('rm ' + path + file)


if __name__ == '__main__':
    delete_directries()
    makeData()
    cmds = ['python groupWeight.py', 'cp -r ../data ../forceInABox/']
    for i in cmds:
        cmd = i
        os.system(cmd)
