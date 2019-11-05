# -*- coding: utf-8 -*-

import os
import csv
import json
from operator import itemgetter


def setSize(data):
    length = len(data['groups'])
    groups = [{'size': 0.0, 'index': i} for i in range(length)]
    for i in range(length):
        groups[i]['size'] = data['groups'][i]['dx'] * data['groups'][i]['dy']
    groups.sort(key=itemgetter('size'))
    data['node2ndMax'] = groups[length - 3]['index']
    data['node3rdMax'] = groups[length - 4]['index']
    data['node2ndMin'] = groups[1]['index']
    data['node3rdMin'] = groups[2]['index']
    return data


def setLink(data):
    links = [{'size': 0, 'index': i} for i in range(len(data['groups']))]
    linkouts = [{'size': 0, 'index': i} for i in range(len(data['groups']))]
    for link in data['links']:
        if data['nodes'][link['source']]['group'] == data['nodes'][link['target']]['group']:
            links[data['nodes'][link['source']]['group']]['size'] += 1
        else:
            linkouts[data['nodes'][link['source']]['group']]['size'] += 1
            linkouts[data['nodes'][link['target']]['group']]['size'] += 1

    links.sort(key=itemgetter('size'))
    data['link2ndMax'] = links[len(data['groups']) - 2]['index']
    data['link3rdMax'] = links[len(data['groups']) - 3]['index']
    data['link2ndMin'] = links[2]['index']
    data['link3rdMin'] = links[3]['index']

    linkouts.sort(key=itemgetter('size'), reverse=True)
    data['linkOut2nd'] = linkouts[1]['index']
    data['linkOut3rd'] = linkouts[2]['index']
    return data


def main():
    origin = '../src/data/'
    for task in os.listdir(origin):
        if task != '.DS_Store':
            for file in os.listdir(origin + task):
                if file != '.DS_Store':
                    data = json.load(open(origin + task + '/' + file, 'r'))
                    data = setSize(data)
                    data = setLink(data)
                    f = open(origin + task + '/' + file, 'w')
                    json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


if __name__ == '__main__':
    main()
