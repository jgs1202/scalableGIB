# -*- coding: utf-8 -*-

import os
import sys
import json
from add_coordinates import calculation


class pheotype32setting(object):
    def __init__(self):
        self.names = []
        self.seasons = []
        self.xs = []
        self.ys = []
        self.dxs = []
        self.dys = []
        self.width = 960
        self.height = 600
        self.set_data()

    def set_data(self):
        self.names = ['AB', 'P1', 'ABa', 'ABp', 'EMS', 'P2', 'ABal', 'Abar', 'ABpl', 'ABpr', 'E', 'MS', 'C', 'P3', 'ABala', 'ABalp', 'ABara', 'ABarp', 'ABpla', 'ABplp', 'ABpra', 'ABprp', 'Ea', 'Ep', 'MSa', 'MSp', 'Ca', 'Cp', 'D', 'ABalaa', 'ABalap', 'ABalpa', 'ABalpp', 'ABaraa', 'ABarap', 'ABarpa', 'ABarpp', 'ABplaa', 'ABplap', 'ABplpa', 'ABplpp', 'ABpraa', 'ABprap', 'ABprpa', 'ABprpp', 'MSaa', 'MSap', 'MSpa', 'MSpp', 'Caa', 'Cap', 'Cpa', 'Cpp', 'ABalaaa', 'ABalapa', 'ABalapp', 'ABalpaa', 'ABalpap', 'ABaraaa', 'ABaraap', 'ABarapa', 'ABarpaa', 'ABarpap', 'ABarppp', 'ABplaaa', 'ABplaap', 'ABplapp', 'ABplpap', 'ABplppa', 'ABplppp', 'ABpraap', 'ABprapa', 'ABprapp', 'ABprapaa', 'ABprpap', 'ABprpap']
        self.xs = [0., 2 * self.width/3, 0., self.width/3, 2 * self.width/3, 2 * self.width/3 + 6/11 * self.width/3, 0., self.width/6, self.width/3, ]
        self.ys = []
        self.dxs = []
        self.dys = []

def process(setting, path):
    graph = json.load(open(path, 'r'))
    group_names = [setting.seasons[i] + ', ' + setting.names[i] for i in range(len(setting.names))]
    rm_list = ['2-4 cell, P0', '4-8 cell, P0', '4-8 cell, AB', '4-8 cell, P1', "4-8 cell, ABal", "4-8 cell, ABar", "4-8 cell, ABpl", "4-8 cell, ABpr"]

    print(len(graph['links']), len(graph['nodes']), len(graph['groups']))
    graph['links'] = [link for link in graph['links'] if graph['nodes'][link['source']]['group'] not in rm_list and graph['nodes'][link['target']]['group'] not in rm_list]
    graph['nodes'] = [node for node in graph['nodes'] if node['group'] not in rm_list and node['group'] not in rm_list]
    graph['groups'] = [group for group in graph['groups'] if group['name'] not in rm_list]
    print(len(graph['links']), len(graph['nodes']), len(graph['groups']))

    for i in range(len(graph['links'])):
        graph['links'][i]['id'] = i
    for i in range(len(graph['nodes'])):
        graph['nodes'][i]['id'] = i
    for i in range(len(graph['groups'])):
        graph['groups'][i]['id'] = i

    for group in graph['groups']:
        if group['name'] not in group_names:
            print(group['name'])
            sys.exit()
        index = group_names.index(group['name'])
        group['x'] = setting.xs[index]
        group['y'] = setting.ys[index]
        group['dx'] = setting.dxs[index]
        group['dy'] = setting.dys[index]

    graph['groupSize'] = len(graph['groups'])
    dic = {'id': len(graph['groups']), 'x': 0, 'y': 0, 'dx': 960, 'dy': 600}
    graph['groups'].append(dic)

    out_file = path[:-5] + '-origin-layout.json'
    f = open(out_file, 'w')
    json.dump(graph, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    f.close()

    from_rust = '../../crest/' + out_file[3:]
    os.chdir('/Users/Aoyama/Documents/Program/scalable-GIB/data_generation/rust-fd-layout/')
    cmd = 'cargo run --release --example gib-cli -- -f ' + from_rust + ' > ' + from_rust[:-5] + '-nodes.txt'
    os.system(cmd)
    os.chdir('/Users/Aoyama/Documents/Program/scalable-GIB/crest/py/')
    data = json.load(open(out_file, 'r'))
    f = open(out_file[:-5] + '-nodes.txt')
    txt = f.read()
    layout = 'origin'
    calculation(data, txt, layout, None, out_file)
    cmd = 'rm ' + out_file[:-5] + '-nodes.txt'
    os.system(cmd)

if __name__ == '__main__':
    setting = pheotype32setting()
    path_05 = '../data/phenotype64-thre0.8.json'
    path_07 = '../data/phenotype64-thre0.9.json'
    process(setting, path_05)
    process(setting, path_07)
