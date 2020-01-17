# -*- coding: utf-8 -*-

import pandas as pd
import json


def txt_to_list(path):
    with open(path) as f:
        txt = f.read()
    _ls = txt.split('\n')
    ls = []
    for i in range(len(_ls)):
        ls.extend(_ls[i].split('\t'))
    for i in range(len(ls)):
        if len(ls[i]) == 0:
            del ls[i]
    return ls


def read_csv(path):
    return pd.read_csv(path)


def graph_init():
    self = {}
    self['groups'] = []
    self['nodes'] = []
    self['links'] = []
    return self


def to_32graph(nodes, links, groups):
    node_group_names = [groups['name'][i] for i in range(len(groups))]
    rm_list = ['2-4 cell, P0', '4-8 cell, P0', '4-8 cell, AB', '4-8 cell, P1', "4-8 cell, ABal", "4-8 cell, ABar", "4-8 cell, ABpl", "4-8 cell, ABpr"]
    group_names = []
    graph = graph_init()

    for node in nodes:
        if node in node_group_names:
            index = node_group_names.index(node)
            group = group_data32['time_group'][index] + ", " + group_data32['cell'][index]
            if group in rm_list:
                continue
            if group not in group_names:
                group_names.append(group)
                dic = {}
                dic['name'] = group
                dic['id'] = len(graph['groups'])
                dic['x'] = 0
                dic['y'] = 0
                dic['dx'] = 0
                dic['dy'] = 0
                graph['groups'].append(dic)

            group_id = group_names.index(group)
            dic = {}
            dic['name'] = node
            dic['id'] = len(graph['nodes'])
            dic['group'] = group_id
            dic['cx'] = 0
            dic['cy'] = 0
            graph['nodes'].append(dic)

    valid_node_list = [node['name'] for node in graph['nodes']]
    for index in range(int(len(links) / 4)):
        dic = {}
        source = links[index * 4]
        target = links[index * 4 + 1]
        if source in valid_node_list and target in valid_node_list:
            dic['source'] = valid_node_list.index(source)
            dic['target'] = valid_node_list.index(target)
            dic['value'] = abs(float(links[index * 4 + 2]))
            dic['id'] = len(graph['links'])
            graph['links'].append(dic)
    graph['groupSize'] = len(graph['groups'])
    graph['nodeSize'] = len(graph['nodes'])
    graph['linkSize'] = len(graph['links'])

    f = open('../data/phenotype32-thre0.5.json', 'w')
    json.dump(graph, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()

    graph['links'] = [link for link in graph['links'] if link['value'] > 0.7]
    for num in range(len(graph['links'])):
        graph['links'][num]['id'] = num
    f = open('../data/phenotype32-thre0.7.json', 'w')
    json.dump(graph, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


def to_64graph(node64, link64):
    node_names = [node for node in node64['FeatureName']]
    group_names = []

    graph = graph_init()
    for i in range(len(node64)):
        dic = {}
        dic['name'] = node64['FeatureName'][i]
        dic['id'] = i
        if node64['CellName'][i] not in group_names:
            dic['group'] = len(group_names)
            group_dic = {}
            group_dic['id'] = len(group_names)
            group_dic['name'] = node64['CellName'][i]
            graph['groups'].append(group_dic)
            group_names.append(node64['CellName'][i])
        else:
            dic['group'] = group_names.index(node64['CellName'][i])
        graph['nodes'].append(dic)

    for i in range(len(link64)):
        source_name = link64['Feature1'][i]
        target_name = link64['Feature2'][i]
        value = link64['Correlation'][i]
        dic = {}
        dic['source'] = node_names.index(source_name)
        dic['target'] = node_names.index(target_name)
        dic['value'] = abs(value)
        dic['id'] = i
        graph['links'].append(dic)
    graph['groupSize'] = len(graph['groups'])

    f = open('../data/phenotype64-all.json', 'w')
    json.dump(graph, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()

    graph['links'] = [link for link in graph['links'] if link['value'] > 0.5]
    for num in range(len(graph['links'])):
        graph['links'][num]['id'] = num
    f = open('../data/phenotype64-thre0.5.json', 'w')
    json.dump(graph, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()

    graph['links'] = [link for link in graph['links'] if link['value'] > 0.7]
    for num in range(len(graph['links'])):
        graph['links'][num]['id'] = num
    f = open('../data/phenotype64-thre0.7.json', 'w')
    json.dump(graph, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()

    graph['links'] = [link for link in graph['links'] if link['value'] > 0.8]
    for num in range(len(graph['links'])):
        graph['links'][num]['id'] = num
    f = open('../data/phenotype64-thre0.8.json', 'w')
    json.dump(graph, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()

    graph['links'] = [link for link in graph['links'] if link['value'] > 0.9]
    for num in range(len(graph['links'])):
        graph['links'][num]['id'] = num
    f = open('../data/phenotype64-thre0.9.json', 'w')
    json.dump(graph, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()


if __name__ == '__main__':
    node32_path = '../data/nodeName.txt'
    link32_path = '../data/links.txt'
    group_data_path = '../data/mst_phenotypes.csv'
    link64_path = '../data/with64_links.csv'
    node64_path = '../data/with64_nodes.csv'

    nodes32 = txt_to_list(node32_path)
    link32 = txt_to_list(link32_path)
    group_data32 = read_csv(group_data_path)
    to_32graph(nodes32, link32, group_data32)

    node64 = read_csv(node64_path)
    link64 = read_csv(link64_path)
    to_64graph(node64, link64)



    # for node in nodes32:
    #     if node not in group_data32['name']:
    #         print(node)
